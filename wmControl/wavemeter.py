"""
Contains the related class for wavemeter control.
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import ctypes
import logging
from decimal import Decimal
from types import TracebackType
from typing import Any, AsyncGenerator, Awaitable, Callable, Set, Type

try:
    from typing import Self  # type: ignore # Python >=3.11
except ImportError:
    from typing_extensions import Self

import janus

import wmControl.wlmData as wlmData
from async_event_bus import event_bus
from wmControl import wlmConst
from wmControl.data_factory import data_factory
from wmControl.wlmConst import DataPackage, NoWavemeterAvailable, WavemeterException, WavemeterType


def callback(product_id: int, mode: int, int_val: int, double_val: float, result: int) -> None:
    """
    Function called by wlmData.dll via thread.

    Parameters
    ----------
    product_id: int
        Version of the WM. Works like a serial number just not named like it.
    mode: int
        cmi constants defined in wlmConst. Represents the different measurements or state changings of a
        connected wavemeter. For more see wlmConst or manual.
    int_val: int
        Meaning of this depends on mode. Usually the time of a state change in milliseconds.
    double_val: float
        Meaning of this depends on mode. Usually the value of a measurement.
    result: int
        Only relevant if mode is cmiSwitcherChannel. Then it holds the time of switching a channel.
    """
    try:
        package: DataPackage = data_factory.get(mode, product_id, int_val, double_val, result)
    except ValueError:
        logging.getLogger(__name__).debug(
            "Unknown data type received from wavemeter %i: %i | %i | %s.", product_id, mode, int_val, double_val
        )
    else:
        event_bus.publish_sync(str(package.product_id), package)


wavemeter_callback_pointer = ctypes.CFUNCTYPE(
    None,  # return
    ctypes.c_int32,  # product_id
    ctypes.c_int32,  # mode
    ctypes.c_int32,  # int_val
    ctypes.c_double,  # double_val
    ctypes.c_int32,  # result
)(callback)


def _lock_wavemeter(function: Callable[..., Awaitable[Any]]):
    """
    A decorator to ensure the current wavemeter is correctly selected by the DLL.

    Parameters
    ----------
    function:
        The coroutine to be wrapped.
    Returns
    -------
    Callable
        The wrapped coroutine

    """

    async def decorated_function(self, *args, **kwargs):
        async with Wavemeter._lock:
            if Wavemeter._active_id != self.product_id:
                await self._set_active_wavemeter(self.product_id)
            return await function(self, *args, **kwargs)

    return decorated_function


class Wavemeter:
    """
    Control all wavemeters connected to a control-PC.

    Parameters
    ----------
    product_id : int
        Version of the WM. Works like a serial number just not named like it.
    dll_path : str
        The directory path where the wlmData.dll is.
    """

    _active_id: int | None = None
    _lock: asyncio.Lock | None = None
    _connected_wavemeters: set[int] = set()

    @property
    def product_id(self) -> int:
        return self.__product_id

    def __init__(self, product_id, dll_path: str) -> None:
        # Set attributes
        self.__product_id = product_id
        self.__logger = logging.getLogger(__name__)

        self.__threadpool: concurrent.futures.ThreadPoolExecutor | None = None
        self.__event_queue: janus.Queue[DataPackage] | None = None
        self.__callback: ctypes.POINTER | None = None

        # Load dll path
        if wlmData.dll is None:
            wlmData.LoadDLL(dll_path)

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        """
        Connect to the wavemeter.
        """
        if Wavemeter._lock is None:
            # The first wavemeter to connect creates the lock
            Wavemeter._lock = asyncio.Lock()

        async with Wavemeter._lock:
            if self.product_id in Wavemeter._connected_wavemeters:
                raise WavemeterException("Wavemeter already connected.")
            Wavemeter._connected_wavemeters.add(self.product_id)

            if len(Wavemeter._connected_wavemeters) == 1:
                # There is only one wavemeter connected and this is us, so the callback is not registered yet.
                # Do it now.
                try:
                    await self.__register_callback(wlmConst.cNotifyInstallCallbackEx, wavemeter_callback_pointer)
                except Exception:
                    # If there is *any* error, remove the wavemeter from the list of connected wavemeters
                    Wavemeter._connected_wavemeters.discard(self.product_id)
                    # then re-raise the error
                    raise

        self.__threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.__event_queue = janus.Queue()

        try:
            await self.get_application_index()
        except NoWavemeterAvailable:
            # There is no way to tell if the wavemeter is actually available, so we will now try to open the
            # wavemeter GUI application and try again
            await self.open_window(self.product_id)
            await self.get_application_index()

        self.__logger.info("Connected to wavemeter %i.", self.product_id)

    async def disconnect(self) -> None:
        """
        Removes the wavemeter event callback.
        """
        if self.product_id in Wavemeter._connected_wavemeters:
            try:
                # Double-checked locking is OK in asyncio, but not for multithreaded applications. See
                # https://peps.python.org/pep-0583/ , which was withdrawn but highlights the problem.
                if len(Wavemeter._connected_wavemeters) == 1:
                    async with Wavemeter._lock:
                        # Make sure that nobody has connected in the meantime
                        if len(self._connected_wavemeters) == 1:
                            await self.__register_callback(wlmConst.cNotifyRemoveCallback, -1)
            finally:
                # Always remove the wavemeter, no matter what happened
                Wavemeter._connected_wavemeters.discard(self.product_id)
                self.__logger.info("Disconnected from Wavemeter %i.", self.product_id)

    async def __wrapper(self, func: Callable, *args: Any) -> Any:
        """
        This is the actual wrapper, that runs the threaded Linux GPIB lib in the executor and
        returns a future to wait for.
        """
        return await asyncio.get_running_loop().run_in_executor(self.__threadpool, func, wlmData.dll, *args)

    async def cancel_tasks(self, tasks: Set[asyncio.Task]) -> None:
        """
        Cancel all tasks and log any exceptions raised.

        Parameters
        ----------
        tasks: Set[asyncio.Task]
            The tasks to cancel
        """
        try:
            for task in tasks:
                if not task.done():
                    task.cancel()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                # Check for exceptions, but ignore asyncio.CancelledError, which inherits from BaseException not Exception
                if isinstance(result, Exception):
                    raise result
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Error during shutdown of the controller.")

    async def read_events(self) -> AsyncGenerator[DataPackage, None]:
        event: DataPackage
        async for event in event_bus.subscribe(str(self.product_id)):
            yield event

    async def __register_callback(
        self, notification_type: int, callback_pointer: Type[wavemeter_callback_pointer] | int
    ) -> None:
        """Only call this function when locked."""
        await self.__wrapper(wlmData.register_callback, notification_type, callback_pointer)

    @_lock_wavemeter
    async def set_switch_mode(self, enable: bool) -> None:
        await self.__wrapper(wlmData.set_switch_mode, enable)

    @_lock_wavemeter
    async def get_switch_mode(self) -> bool:
        return await self.__wrapper(wlmData.get_switch_mode)

    @_lock_wavemeter
    async def get_wavelength(self, channel: int) -> Decimal:
        return await self.__wrapper(wlmData.get_wavelength, channel)

    @_lock_wavemeter
    async def get_frequency(self, channel: int) -> Decimal:
        return await self.__wrapper(wlmData.get_frequency, channel)

    @_lock_wavemeter
    async def get_channel(self) -> int:
        return await self.__wrapper(wlmData.get_channel)

    @_lock_wavemeter
    async def get_channel_count(self) -> int:
        return await self.__wrapper(wlmData.get_channel_count)

    @_lock_wavemeter
    async def set_channel(self, channel: int) -> None:
        return await self.__wrapper(wlmData.set_channel, channel)

    @_lock_wavemeter
    async def get_wavemeter_info(self) -> tuple[WavemeterType, int, tuple[int, int]]:
        return await self.__wrapper(wlmData.get_wavemeter_info)

    @staticmethod
    def get_wavemeter_count():
        return wlmData.get_wavemeter_count(wlmData.dll)

    @_lock_wavemeter
    async def get_application_index(self) -> int:
        """
        Return the GUI application index of the wavemeter. Warning this function will return wrong values if the
        wavemeter application is not running!

        Parameters
        ----------
        Returns
        -------
        int
            The GUI application index of the wavemeter
        """
        return wlmData.get_wavemeter_index(wlmData.dll, self.product_id)

    async def set_active_wavemeter(self, product_id: int):
        async with Wavemeter._lock:
            await self._set_active_wavemeter(product_id)

    async def _set_active_wavemeter(self, product_id: int):
        await self.__wrapper(wlmData.set_active_wavemeter, product_id)
        Wavemeter._active_id = product_id

    @_lock_wavemeter
    async def get_temperature(self):
        return await self.__wrapper(wlmData.get_temperature)

    @_lock_wavemeter
    async def get_calibration_wavelength(self, pre_calibration: bool = False):
        return await self.__wrapper(wlmData.get_calibration_wavelength, pre_calibration)

    @_lock_wavemeter
    async def open_window(self, product_id: int) -> None:
        """
        Open the GUI window required for the wavemeter DLL access. This function will wait indefinitely for the window
        to open.

        Parameters
        ----------
        product_id: int
            The wavemeter product id/version/serial number.
        """
        # Set the timeout to -1 (infinity), because the timeout should be handled via asyncio
        await self.__wrapper(wlmData.open_window, None, product_id, -1)

    @_lock_wavemeter
    async def set_auto_calibration(self, enable: bool) -> None:
        await self.__wrapper(wlmData.set_auto_calibration_mode, enable)

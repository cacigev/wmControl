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
from typing import Any, AsyncGenerator, Callable, Self, Set, Type

import janus

import wmControl.wlmData as wlmData
from async_event_bus import event_bus
from wmControl import wlmConst
from wmControl.data_factory import data_factory
from wmControl.wlmConst import DataPackage


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
        logging.getLogger(__name__).debug("Unknown data type received: %i.", mode)
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


def _lock_wavemeter(function):
    """
    A decorator to ensure the current wavemeter is correctly selected by the DLL.
    Parameters
    ----------
    function

    Returns
    -------

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
            Wavemeter._lock = asyncio.Lock()
            # If the lock has not been created we need to initialise the callback
            wlmData.dll.Instantiate(
                wlmConst.cInstNotification, wlmConst.cNotifyInstallCallbackEx, wavemeter_callback_pointer, 0
            )

        self.__threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.__event_queue = janus.Queue()

        self.__logger.info("Connected to wavemeter %i.", self.product_id)

    async def disconnect(self) -> None:
        """
        Calling disconnect() does nothing for now.
        """
        wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)
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
    async def get_wavemeter_info(self):
        return await self.__wrapper(wlmData.get_wavemeter_info)

    @_lock_wavemeter
    async def get_wavemeter_count(self):
        return await self.__wrapper(wlmData.get_wavemeter_count)

    async def set_active_wavemeter(self, product_id: int):
        async with Wavemeter._lock:
            await self._set_active_wavemeter(product_id)

    async def _set_active_wavemeter(self, product_id: int):
        await self.__wrapper(wlmData.set_active_wavemeter, product_id)
        Wavemeter._active_id = product_id

    @_lock_wavemeter
    async def get_temperature(self):
        return await self.__wrapper(wlmData.get_temperature)

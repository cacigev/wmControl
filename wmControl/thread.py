import ctypes
import logging
from threading import Event

import janus

from wmControl import wlmConst, wlmData

callbacktype = ctypes.CFUNCTYPE(
    None,
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_double,
    ctypes.c_int32,
)


class Worker:
    """
    Managing the synchronous threads from the wavemeter.

    Attributes
    ----------
    version : int
        Version of the WM. Works like a serial number just not named like it. 0 should call the first activated WM, but
        don't rely on that.
    queue : Queue
        Holds the queue.
    """

    def _create_callback(self, output_queue):
        def callback(ver: int, mode: int, int_val: int, double_val: float, result: int):
            """
            Function called by wlmData.dll via thread.

            Parameters
            ----------
            ver: int
                Version of the WM. Works like a serialnumber just not named like it.
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
            output_queue.put(f"Time:{int_val}, WM:{ver}, Channel:{mode}, Wavelength:{double_val:.8f}, Res1:{result}")

        cb_pointer = callbacktype(callback)

        return cb_pointer

    def run(self, output_queue: janus.SyncQueue[str], shutdown_event: Event) -> None:
        """
        Producer for wavemeter data.

        Uses the vendor solution for threading and writes all measurements or state changings of a connected wavemeter into the queue.

        Parameters
        ----------
        output_queue: janus.SyncQueue[int]
            The synchronus part of the queue, wich was instantiated in control.wavemeter.
        """

        cb_pointer = self._create_callback(output_queue)

        wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallbackEx, cb_pointer, 0)
        self.__logger.info("Connected to host")

        try:
            shutdown_event.wait()
            # There is no more work to be done. Terminate now.
            wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)
            self.__logger.info("Removed callback.")
        finally:
            self.__logger.info("Disconnected from host. Shutting down worker.")

    # Prints all measured frequencies of one WM
    # Unit: THz
    def frequencysProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int) -> None:
        """
        Prints all measurements and state changings of connected wavemeters.

        Parameters
        ----------
        ver: int
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

        Raises
        ------
        ValueError
            If a mode is not writen down in wlmConst but recived via this function.
        """
        const_to_channel = {
            wlmConst.MeasureMode.cmiWavelength1: 1,
            wlmConst.MeasureMode.cmiWavelength2: 2,
            wlmConst.MeasureMode.cmiWavelength3: 3,
            wlmConst.MeasureMode.cmiWavelength4: 4,
            wlmConst.MeasureMode.cmiWavelength5: 5,
            wlmConst.MeasureMode.cmiWavelength6: 6,
            wlmConst.MeasureMode.cmiWavelength7: 7,
            wlmConst.MeasureMode.cmiWavelength8: 8,
        }

        try:
            mode = wlmConst.MeasureMode(mode)
        except ValueError:
            self.__logger.warning(
                "Unknown status received: '%s' is not defined. Parameters: %s, %s, %s, %s, %s",
                mode,
                ver,
                mode,
                int_val,
                double_val,
                result,
            )
        else:
            if (ver == self._version) and (mode in const_to_channel):
                self.__logger.info(
                    "Time: %s, WM: %s, Channel: %s, Frequency: %.8f THz",
                    int_val,
                    ver,
                    const_to_channel[mode],
                    299792.458 / double_val,
                )

    def __init__(self, ver):
        self.__logger = logging.getLogger(__name__)
        self._version = ver
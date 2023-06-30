import asyncio
import ctypes
import logging
import time

import janus

from wmControl import wlmConst, wlmData


class Callback:
    """
    Managing the synchronus threads from the wavemeter.

    Attributes
    ----------
    version : int
        Version of the WM. Works like a serialnumber just not named like it. 0 should call the first activated WM, but dont rely on that.
    queue : Queue
        Holds the queue.
    """
    version = 0
    queue = None

    def callback(self, sync_q: janus.SyncQueue[int]) -> None:
        """
        Producer for wavemeter data.

        Uses the vendor solution for threading and writes all measurements or state changings of a connected wavemeter into the queue.

        Parameters
        ----------
        sync_q: janus.SyncQueue[int]
            The synchronus part of the queue, wich was instantiated in control.wavemeter.
        """

        def helper(ver: int, mode: int, int_val: int, double_val: float, result: int) -> None:
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
                Meaning of this dependts on mode. Usually the time of a state change in miliseconds.
            double_val: float
                Meaning of this dependts on mode. Usually the value of a measurement.
            result: int
                Only relevant if mode is cmiSwitcherChannel. Then it holds the time of switching a channel.
            """
            sync_q.put(f"Time:{int_val}, WM:{ver}, Channel:{mode}, Wavelength:{double_val:.8f}, Res1:{result}")

        callbacktype = ctypes.CFUNCTYPE(
            None,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_double,
            ctypes.c_int32,
        )
        callbackpointer = callbacktype(helper)

        wlmData.dll.Instantiate(
            wlmConst.cInstNotification,
            wlmConst.cNotifyInstallCallbackEx,
            callbackpointer,
            0,
        )

        try:
            sync_q.join()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Thread will be terminated.")
            raise
        finally:
            wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)

    # Prints all measured frequencies of one WM
    # Unit: THz
    def frequencysProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int) -> None:
        """
        Prints all measurements and state changings of connected wavemeters.

        Parameters
        ----------
        ver: int
            Version of the WM. Works like a serialnumber just not named like it.
        mode: int
            cmi constants defined in wlmConst. Represents the different measurements or state changings of a 
            connected wavemeter. For more see wlmConst or manual.
        int_val: int
            Meaning of this dependts on mode. Usually the time of a state change in miliseconds.
        double_val: float
            Meaning of this dependts on mode. Usually the value of a measurement.
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
            if (ver == self.version) and (mode in const_to_channel):
                self.__logger.info(
                    "Time: %s, WM: %s, Channel: %s, Frequency: %.8f THz",
                    int_val,
                    ver,
                    const_to_channel[mode],
                    299792.458 / double_val,
                )

    def __init__(self, ver, wavemeter):
        self.__logger = logging.getLogger(__name__)
        self.version = ver

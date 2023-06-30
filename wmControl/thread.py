import asyncio
import ctypes
import logging
import time

import janus

from wmControl import wlmConst, wlmData


class Callback:
    version = 0
    queue = None

    def callback(self, sync_q: janus.SyncQueue[int]) -> None:
        def helper(ver: int, mode: int, int_val: int, double_val: float, result: int):
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
    def frequencysProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int):
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

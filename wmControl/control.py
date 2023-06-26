# wlmData.dll related imports
from wmControl import wlmData
from wmControl import wlmConst
import ctypes, time

# others
import sys
import numpy as np
from wmControl import thread


class Wavemeter:
    # Set attributes: DLL path, version and callbacktype
    DLL_PATH = "./wmControl/wlmData.dll"
    version = 0  # Version of the WM. Works like a serialnumber just not named like it. 0 should call the first activated WM, but dont rely on that.
    callbacktype = ctypes.CFUNCTYPE(
        None,
        ctypes.c_int32,
        ctypes.c_int32,
        ctypes.c_int32,
        ctypes.c_double,
        ctypes.c_int32,
    )  # Defining which kind of Parameters is passed to instantiate.

    # Attributes of buffer and buffer
    bfr_length = 5  # buffer length
    bfr_pntr = 0
    bfr = np.zeros(
        [bfr_length, 3], dtype=int
    )  # The buffer of length bfr_length. Buffer elements that didnt recieved WM-data are left -3.0.

    # Instantiate thread
    threadCall = None

    def wavelengths(self, measure_time):
        callbackpointer = self.callbacktype(self.threadCall.wavelengthsProcEx)
        wlmData.dll.Instantiate(
            wlmConst.cInstNotification,
            wlmConst.cNotifyInstallCallbackEx,
            callbackpointer,
            0,
        )  # instantiate thread

        # Wait for events (wavelength) until the acquisition time has passed
        time.sleep(measure_time)
        # print(self.bfr)

        wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)  # remove thread
        print("Done")

    def frequencys(self, measure_time):
        callbackpointer = self.callbacktype(self.threadCall.frequencysProcEx)
        wlmData.dll.Instantiate(
            wlmConst.cInstNotification,
            wlmConst.cNotifyInstallCallbackEx,
            callbackpointer,
            0,
        )  # instantiate thread

        # Wait for events (frequency) until the acquisition time has passed
        time.sleep(measure_time)
        # print(self.bfr)

        wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)  # remove thread
        print("Done")

    def allwavelengths(self, measure_time):
        callbackpointer = self.callbacktype(self.threadCall.allwavelengthsProcEx)
        wlmData.dll.Instantiate(
            wlmConst.cInstNotification,
            wlmConst.cNotifyInstallCallbackEx,
            callbackpointer,
            0,
        )  # instantiate thread

        # Wait for events (wavelength) until the acquisition time has passed
        time.sleep(measure_time)
        # print(self.bfr)

        wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)  # remove thread
        print("Done")

    def getSwitcher(self, measure_time):
        # switcher mode funktioniert nicht in quips b: GetSwitcherMode liefert 0 unabhängig davon ob switcher mode aktiv ist oder nicht
        # grund nicht bekannt
        if False:  # wlmData.dll.GetSwitcherMode(0) == 0):
            print(wlmData.dll.GetSwitcherMode(0))
            print("Error: Switcher mode is not active or not avaible for this WM.")
        else:
            print(wlmData.dll.GetSwitcherMode(0))
            callbackpointer = self.callbacktype(self.threadCall.getSwitchedChannel)
            wlmData.dll.Instantiate(
                wlmConst.cInstNotification,
                wlmConst.cNotifyInstallCallbackEx,
                callbackpointer,
                0,
            )  # instantiate thread

            # Wait for events (switching channels) until the aquisaition time has passed
            time.sleep(measure_time)
            # print(self.bfr)

            wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, -1, 0)  # remove thread
            print("Done")

    def putBfr(self, itm):
        # FIXME: Not thread-safe, but called from threads!
        # For Asyncio check out Janus: https://github.com/aio-libs/janus
        # else use queue: https://docs.python.org/3/library/queue.html
        if self.bfr_pntr == self.bfr_length:
            self.bfr[0] = itm
            self.bfr_pntr = 1
            print(self.bfr, self.bfr_pntr)
            return
        self.bfr[self.bfr_pntr] = itm
        self.bfr_pntr += 1
        print(self.bfr, self.bfr_pntr)

    def __init__(self, ver, length=5, dll=".Wavemeter/wmControl/wlmData.dll"):
        # Set attributes
        self.DLL_PATH = dll
        self.version = ver
        self.bfr_length = length

        # instantiate usercalls
        self.threadCall = thread.Callback(ver, self)

        # Load DLL Path
        try:
            wlmData.LoadDLL(self.DLL_PATH)
        except:
            sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % self.DLL_PATH)

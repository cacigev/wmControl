import asyncio
import ctypes
import sys
import time

import janus
import numpy as np

from wmControl import thread, wlmConst, wlmData


class Wavemeter:
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

    async def async_coro(self, async_q: janus.AsyncQueue[int]) -> None:
        i = 0
        while "not terminated":
            val = await async_q.get()
            print(i, val)
            i += 1
            async_q.task_done()

    async def main(self) -> None:
        queue: janus.Queue[int] = janus.Queue()
        loop = asyncio.get_running_loop()
        # print("hello")
        try:
            fut = loop.run_in_executor(None, self.threadCall.callback, queue.sync_q)
            await self.async_coro(queue.async_q)
            await fut
            queue.close()
            await queue.wait_closed()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Thread is terminated.")

    def __init__(self, ver, dll_path, start_main=False, length=5):
        # Set attributes
        self.DLL_PATH = dll_path
        self.version = ver
        self.bfr_length = length

        # instantiate user calls
        self.threadCall = thread.Callback(ver, self)

        # Load DLL Path
        try:
            wlmData.LoadDLL(self.DLL_PATH)
        except:
            sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % self.DLL_PATH)

        # instantiate queue and loop
        if start_main:
            asyncio.run(self.main())

"""
Contains the related classes for wavemeter control.
"""

import asyncio
import ctypes
import sys
import time

import janus
import numpy as np

from wmControl import thread, wlmConst, wlmData


class Wavemeter:
    """
    Control all wavemeters connected to a control-PC.

    Attributes
    ----------
    dll_path : str
        The directory path where the wlmData.dll is.
    version : int
        Version of the WM. Works like a serialnumber just not named like it.
    callbacktype : function
        Returning funtion prototype. Defining which kind of Parameters is passed to instantiate.

    Parameters
    ----------
    ver : int
        Version of the WM. Works like a serialnumber just not named like it.
    dll_path : str
        The directory path where the wlmData.dll is.
    start_main : bool, default False
        Switch the asynchronus/synchronus queue code on and off. Used for debugging.
    length : int, default 5
        Buffer length. Obsolet.
    """

    # Set attributes: DLL path, version and callbacktype
    dll_path = "./wmControl/wlmData.dll"
    version = 0 #  0 should call the first activated WM, but dont rely on that.
    callbacktype = ctypes.CFUNCTYPE(
        None,
        ctypes.c_int32,
        ctypes.c_int32,
        ctypes.c_int32,
        ctypes.c_double,
        ctypes.c_int32,
    )

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
        """
        Consumer of queue.

        Takes the data queue and (should) pick relevant information.

        Parameter
        ---------
        async_q: janus.AsyncQueue[int]
            Asynchronus part of the queue wich is instantiated via control.wavemeter.
        """
        i = 0
        while "not terminated":
            val = await async_q.get()
            print(i, val)
            i += 1
            async_q.task_done()

    async def main(self) -> None:
        """
        Manages synchronus and asynchronus part of the queue.
        """
        queue: janus.Queue[int] = janus.Queue()
        loop = asyncio.get_running_loop()
        try:
            fut = loop.run_in_executor(None, self.threadCall.callback, queue.sync_q)
            await self.async_coro(queue.async_q)
            await fut
            queue.close()
            await queue.wait_closed()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Thread is terminated.")

    def __init__(self, ver: int, dll_path: str, start_main: bool=False, length: int=5) -> None:
        # Set attributes
        self.dll_path = dll_path
        self.version = ver
        self.bfr_length = length

        # instantiate user calls
        self.threadCall = thread.Callback(ver, self)

        # Load dll path
        try:
            wlmData.LoadDLL(self.dll_path)
        except:
            sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % self.DLL_PATH)

        # instantiate queue and loop
        if start_main:
            asyncio.run(self.main())

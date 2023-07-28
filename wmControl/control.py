"""
Contains the related classes for wavemeter control.
"""

import asyncio
import logging
import sys
import threading
from contextlib import AsyncExitStack
from typing import Set

import janus

from wmControl import wlmData
from .data_factory import data_factory
from wmControl.thread import Worker
from wmControl.wlmConst import DataPackage


class Wavemeter:
    """
    Control all wavemeters connected to a control-PC.

    Attributes
    ----------
    dll_path : str
        The directory path where the wlmData.dll is.
    version : int
        Version of the WM. Works like a serial number just not named like it.

    Parameters
    ----------
    ver : int
        Version of the WM. Works like a serialnumber just not named like it.
    dll_path : str
        The directory path where the wlmData.dll is.
    """

    version = 0  # 0 should call the first activated WM, but don't rely on that.

    async def async_coro(self, async_q: janus.AsyncQueue[DataPackage]) -> None:
        """
        Consumer of queue.

        Takes the data queue and (should) pick relevant information.

        Parameter
        ---------
        async_q: janus.AsyncQueue[DataPackage]
            Asynchronous part of the queue.
        """
        i = 0
        try:
            while "not terminated":
                val = await async_q.get()
                print(i, val)
                i += 1
                async_q.task_done()
        finally:
            self.__logger.info("Consumer shut down.")

    async def cancel_tasks(self, tasks: Set[asyncio.Task], shutdown_event: threading.Event) -> None:
        """
        Cancel all tasks and log any exceptions raised.

        Parameters
        ----------
        tasks: Set[asyncio.Task]
            The tasks to cancel
        shutdown_event : threading.Event
            shutdown
        """
        shutdown_event.set()
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

    async def producer(self, result_queue, input_queue, shutdown_event):
        sync_worker = Worker(self.version)
        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                sync_worker.run,
                result_queue,
                input_queue,
                shutdown_event
            )
        except asyncio.CancelledError:
            pass
        finally:
            print("producer done!")

    async def main(self) -> None:
        """
        Manages synchronous and asynchronous part of the queue.
        """
        # parse input
        result_queue: janus.Queue[str] = janus.Queue()
        shutdown_event: threading.Event = threading.Event()
        input_queue = [1, 2, 3, 4, 5, None]
        async with AsyncExitStack() as stack:
            tasks: set[asyncio.Task] = set()
            stack.push_async_callback(self.cancel_tasks, tasks, shutdown_event)

            producer = asyncio.create_task(self.producer(result_queue.sync_q, input_queue, shutdown_event))
            tasks.add(producer)
            consumer = asyncio.create_task(self.async_coro(result_queue.async_q))
            tasks.add(consumer)

            await asyncio.gather(*tasks)

    def __init__(self, ver, dll_path: str, length=5) -> None:
        # Set attributes
        self.dll_path = dll_path
        self.version = ver
        self.bfr_length = length
        self.__logger = logging.getLogger(__name__)

        # Load dll path
        wlmData.LoadDLL(self.dll_path)

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
from wmControl.thread import InputWorker
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
        Version of the WM. Works like a serial number just not named like it.
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
                print("consumer:", i, val)
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

    async def producer(self,
                       result_queue: janus.AsyncQueue[DataPackage],
                       input_queue: janus.AsyncQueue[DataPackage],
                       request,
                       shutdown_event: threading.Event
                       ) -> None:
        """
        Producer of queue.

        Starts thread and gather data.

        Parameter
        ---------
        result_queue
            Data queue of relevant information.
        input_queue : janus.AsyncQueue[DataPackage]
            Request of the user.
        helper_queue : janus.AsyncQueue[DataPackage]
            Temporarily stores data. Internal use only.
        """
        sync_worker = Worker(self.version)
        helper_queue: janus.Queue[DataPackage] = janus.Queue()
        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                sync_worker.run,
                result_queue,
                input_queue,
                helper_queue.sync_q,
                request,
                shutdown_event
            )
        except asyncio.CancelledError:
            pass
        finally:
            print("producer done!")

    def helper(self, input_queue) -> None:
        """
        Helper simulating input.
        :param input_queue:
        :return:
        """
        input_queue.put(95)  # 0
        input_queue.put(95)  # 1
        input_queue.put(95)  # 2

        input_queue.put(14)  # 3
        input_queue.put(95)  # 4
        input_queue.put(95)  # 5

        input_queue.put(95)  # 6
        input_queue.put(42)  # 7
        input_queue.put(14)  # 8

        input_queue.put(95)  # 9
        input_queue.put(95)  # 10
        input_queue.put(95)  # 11

        input_queue.put(None)

    async def start_producers(self, result_queue, input_queue, shutdown_event):
        """
        Starts worker for every unique request.
        """
        worker_list: [int] = []
        request: int = input_queue.get()  # Will turn to Datapackage
        tasks: set[asyncio.Task] = set()
        while request:
            print("Request: ", request)
            if request in worker_list:  # Will turn to request.mode
                print("Producer already started")
                pass
            else:
                print("Start producer")
                worker_list.append(request)  # Will turn to request.mode
                tasks.add(
                    asyncio.create_task(self.producer(result_queue, input_queue, request, shutdown_event))
                )
            request = input_queue.get()
            print("Next request: ", request, "\n")
        print("Starting producers finished")

        await asyncio.gather(*tasks)

    async def main(self) -> None:
        """
        Manages synchronous and asynchronous part of the queue.
        """
        result_queue: janus.Queue[DataPackage] = janus.Queue()
        shutdown_event: threading.Event = threading.Event()
        input_queue: janus.Queue[DataPackage] = janus.Queue()
        self.helper(input_queue.sync_q)  # simulating input
        # async with AsyncExitStack() as stack:
        tasks: set[asyncio.Task] = set()
        # stack.push_async_callback(self.cancel_tasks, tasks, shutdown_event)

        start_producers = asyncio.create_task(self.start_producers(
            result_queue.async_q,
            input_queue.sync_q,
            shutdown_event
        ))
        tasks.add(start_producers)
        # producer = asyncio.create_task(self.producer(
        #     result_queue.sync_q,
        #     input_queue.sync_q,
        #     95,
        #     shutdown_event
        # ))
        # tasks.add(producer)

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

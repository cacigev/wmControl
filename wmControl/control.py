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
from wmControl.wlmConst import MeasureMode


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

    async def async_coro(
            self,
            async_q: janus.AsyncQueue[DataPackage],
            expected_reply: dict[str, [int]]
    ) -> None:
        """
        Consumer of queue.

        Takes the data queue and (should) pick relevant information.

        Parameter
        ---------
        async_q: janus.AsyncQueue[DataPackage]
            Asynchronous part of the result queue.
        expected_reply: dict[str, [int]]
            Holds expected data and id of dedicated request
        """
        i = 0
        try:
            while "not terminated":
                val = await async_q.get()
                try:
                    if str(val.mode) in expected_reply:
                        request_id = expected_reply[str(val.mode)].pop(0)
                        print(f"{request_id:04}: {val}")
                except:
                    expected_reply.pop(str(val.mode))
                # print("consumer:", i, val)
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
                       result_queue: janus.SyncQueue[DataPackage],
                       future_queue: janus.SyncQueue[DataPackage],
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
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                sync_worker.run,
                result_queue,
                future_queue,
                shutdown_event,
            )
        except asyncio.CancelledError:
            pass
        finally:
            print("producer done!")

    # im producer werden futures erwartet. wenn future erledigt wurde, wird die zu run übergebene liste um future erleichtert
    # set_result geschieht im producer
    # list.remove(); erstes element

    def helper(self, input_queue, future_queue) -> None:
        """
        Helper simulating input.
        :param input_queue:
        :return:
        """
        input_queue.put(MeasureMode.cmiWavelength8)  # 0
        input_queue.put(MeasureMode.cmiWavelength8)  # 1
        input_queue.put(MeasureMode.cmiWavelength8)  # 2

        input_queue.put(MeasureMode.cmiTemperature)  # 3
        input_queue.put(MeasureMode.cmiWavelength8)  # 4
        input_queue.put(MeasureMode.cmiWavelength8)  # 5

        input_queue.put(MeasureMode.cmiWavelength8)  # 6
        input_queue.put(MeasureMode.cmiWavelength1)  # 7
        input_queue.put(MeasureMode.cmiTemperature)  # 8

        input_queue.put(MeasureMode.cmiWavelength8)  # 9
        input_queue.put(MeasureMode.cmiWavelength8)  # 10
        input_queue.put(MeasureMode.cmiWavelength8)  # 11

        input_queue.put(None)

        loop = asyncio.get_running_loop()
        for i in range(13):
            future_queue.put(loop.create_future())
        future_queue.put(None)

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

    async def input_consumer(
            self,
            input_queue: janus.SyncQueue[int],
            expected_reply: dict[str, [int]]
    ) -> None:
        request_id = 0
        request = input_queue.get()
        while request:
            request = str(request)
            print("Request: ", request)
            if request in expected_reply:  # Will turn to request.mode
                print("Add request id to id list")
                expected_reply[request].append(request_id)
                print("expect:", expected_reply[request])
            else:
                print("Add request to expected reply")
                expected_reply[request] = [request_id]
                print("expect:", expected_reply[request])
            request = input_queue.get()
            request_id += 1
            print("Next request: ", request, "\n")

    async def main(self) -> None:
        """
        Manages synchronous and asynchronous part of the queue.
        """
        result_queue: janus.Queue[DataPackage] = janus.Queue()
        shutdown_event: threading.Event = threading.Event()
        input_queue: janus.Queue[DataPackage] = janus.Queue()
        future_queue: janus.Queue[asyncio.Future] = janus.Queue()
        self.helper(input_queue.sync_q, future_queue.sync_q)
        expected_reply = {}
        async with AsyncExitStack() as stack:
            tasks: set[asyncio.Task] = set()
            stack.push_async_callback(self.cancel_tasks, tasks, shutdown_event)

            input_consumer = asyncio.create_task(self.input_consumer(
                input_queue.sync_q,
                expected_reply
            ))
            tasks.add(input_consumer)

            producer = asyncio.create_task(self.producer(
                result_queue.sync_q,
                future_queue.sync_q,
                shutdown_event
            ))
            tasks.add(producer)

            consumer = asyncio.create_task(self.async_coro(result_queue.async_q, expected_reply))
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

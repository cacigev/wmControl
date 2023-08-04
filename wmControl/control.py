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

    async def result_consumer(
            self,
            result_queue: janus.AsyncQueue[DataPackage],
            expected_reply: dict[MeasureMode: [asyncio.Future]]
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
        # i = 0
        try:
            while "not terminated":
                reply = await result_queue.get()
                try:
                    if reply.mode in expected_reply:
                        value: asyncio.Future = await expected_reply[reply.mode].pop(0)
                        value.set_result(reply)
                        print("%s", value)
                except IndexError:
                    expected_reply.pop(reply.mode)
                # print("consumer:", i, reply)
                # i += 1
                # result_queue.task_done()
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
                       job_queue: janus.SyncQueue[DataPackage]
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
                job_queue
            )
        except asyncio.CancelledError:
            pass
        finally:
            print("producer done!")

    def helper(
            self,
            input_queue: janus.SyncQueue
    ) -> None:
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

    async def input_consumer(
            self,
            input_queue: janus.AsyncQueue[MeasureMode],
            expected_reply: dict[str: [int]]
    ) -> None:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        jobs: set[asyncio.Future] = set()
        while "Input queue not empty":
            request: MeasureMode = await input_queue.get()
            fut: asyncio.Future = loop.create_future()
            if request in expected_reply:
                expected_reply[request].append(fut)
            else:
                expected_reply[request] = [fut]
            jobs.add(fut)
            if input_queue.empty():
                break
        print('foo')
        await asyncio.gather(*jobs)
        print('bar')
        await input_queue.put(None)

    async def main(self) -> None:
        """
        Manages synchronous and asynchronous part of the queue.
        """
        print("--------------------------------------------------")  # Separates NetAccessServer messages from control.
        result_queue: janus.Queue[DataPackage] = janus.Queue()
        expected_reply = {}
        # Simulating input ------------
        input_queue: janus.Queue[DataPackage] = janus.Queue()
        self.helper(input_queue.sync_q)
        # job_queue: janus.Queue[asyncio.Future] = janus.Queue()
        # -----------------------------
        print("--------------------------------------------------")
        # async with AsyncExitStack() as stack:
        tasks: set[asyncio.Task] = set()
        # stack.push_async_callback(self.cancel_tasks, tasks, shutdown_event)

        input_consumer = asyncio.create_task(self.input_consumer(input_queue.async_q, expected_reply))
        tasks.add(input_consumer)

        producer = asyncio.create_task(self.producer(
            result_queue.sync_q,
            input_queue.sync_q
        ))
        tasks.add(producer)

        result_consumer = asyncio.create_task(self.result_consumer(
            result_queue.async_q,
            expected_reply
        ))
        tasks.add(result_consumer)

        await asyncio.gather(*tasks)

    def __init__(self, ver, dll_path: str, length=5) -> None:
        # Set attributes
        self.dll_path = dll_path
        self.version = ver
        self.bfr_length = length
        self.__logger = logging.getLogger(__name__)

        # Load dll path
        wlmData.LoadDLL(self.dll_path)

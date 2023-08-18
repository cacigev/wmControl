from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import time
from typing import Any
import os

import numpy as np
from scpi import Commands, decode_IDN, split_line


class MakeFile:

    def create_scpi_protocol(self) -> Commands:
        """"""
        return Commands(
            {
                "MEASure:WAVElength:CHannel": "CH:x/nm",
                "MEASure:WAVElength": "CH:x/nm",
                "MEASure:FREQuency:CHannel": "CH:x/THz",
                "MEASure:FREQuency": "CH:x/THz",
                "MEASure:TEMPerature": "T/°C",
            }
        )


    def __init__(
            self,
            filename: str,
            clients: [[str]],
            measure_time: int=0,
            repeat_count: int=0,
            sleep: int=0,
            additional_info: str | None=None,
            column_names: [str] | None=None,
    ):
        """
        Parameter
        ---------
        filename: str | None =None
            Name of file to save the data. If none is given the default will be used.
            If the default filename is None the user will be asked to give a filename via input.
        """
        self.filename: str = filename
        # time infos
        self.time_connected: datetime = datetime.now()
        self.time_started: datetime | None = None
        self.time_stopped: datetime | str = "NaN"
        # repeat infos
        self.repeat_measure_time: int = measure_time
        self.repeat_count: int = repeat_count
        self.repeat_sleep: int = sleep
        # header elements
        self.time_info: str = ""
        self.wavemeter_info: str = "Listen to WM: "
        self.repeat_info: str = ""
        self.additional_info: str | None = additional_info
        self.header: str = ""

        if not self.filename[-4:] == ".txt":
            self.filename = self.filename + ".txt"
        if additional_info:
            self._set_additional_info(additional_info)
        if column_names:
            self.set_column_names(*column_names)
        else:
            self.column_names: str = "t/s   T/°C    CH:1/nm"

        self.set_time_started()
        self._set_time_info()
        self._set_wavemeter_info(*clients)
        self._set_repeat_info()
        self.set_header()


    def set_column_names(self, request: str) -> None:
        column_names: str = "t/s"
        protocol = self.create_scpi_protocol()
        commands: [str] = request.split("\n")
        for command in commands:
            scpi_requests = split_line(command)

            for scpi_request in scpi_requests:
                column_name = protocol[scpi_request.name]
                column_names += f"   {column_name}"

        # TODO: add arguments

        self.column_names = column_names
        self.set_header()


    def set_time_started(self, time_started: datetime | str | int | None=None) -> None:
        if time_started:
            self.time_started = str(time_started)
        else:
            self.time_started = datetime.now()

        self._set_time_info()


    def set_time_stopped(self, time_stopped: datetime | int) -> None:
        self.time_stopped = time_stopped

        self._set_time_info()


    def set_repeat_measure_time(self, value: int) -> None:
        if value:
            self.repeat_measure_time = value
            self._set_repeat_info()

    def set_repeat_count(self, value: int) -> None:
        if value:
            self.repeat_count = value
            self._set_repeat_info()


    def set_repeat_sleep(self, value: int) -> None:
        if value:
            self.repeat_sleep = value
            self._set_repeat_info()


    def _set_time_info(self) -> None:
        time_info: str = "Connected: x  Started: x Stopped: x"
        # Maybe if-clause to not write None in time_stopped if its None
        time_info = time_info.replace("x", str(self.time_connected), 1)
        time_info = time_info.replace("x", str(self.time_started), 1)
        time_info = time_info.replace("x", str(self.time_stopped), 1)

        self.time_info = time_info
        self.set_header()


    def _set_wavemeter_info(self, *wavemeter_info: [str]) -> None:
        for wm in wavemeter_info:
            product = wm[0]
            product_id = decode_IDN(product)["model"]
            self.wavemeter_info += product_id + "   "

        self.set_header()


    def _set_additional_info(self, info: str) -> None:
        self.additional_info = info

        self.set_header()


    def _set_repeat_info(self) -> None:
        repeat_info: str = "Repeat: x Measure_time: x Sleep: x"
        repeat_info = repeat_info.replace("x", str(self.repeat_count), 1)
        repeat_info = repeat_info.replace("x", str(self.repeat_measure_time), 1)
        repeat_info = repeat_info.replace("x", str(self.repeat_sleep), 1)

        self.repeat_info = repeat_info
        self.set_header()


    def set_header(self) -> None:
        header: str = "x\nx\n\nx\n\nx"
        header = header.replace("x", str(self.time_info), 1)
        header = header.replace("x", str(self.wavemeter_info), 1)
        header = header.replace("x", str(self.repeat_info), 1)
        header = header.replace("x", str(self.column_names), 1)

        self.header = header


    def get_header(self) -> str:
        return self.header

    def write_txt_file(self, data: [float], fmt: [str] | None=None) -> None:
        header: str = ""
        if not os.path.isfile(self.filename):  # checks if file already exists
            header = self.header
        if fmt is None:
            fmt = ("%i", "%.3f", "%.8f", "%.8f", "%.8f", "%.8f")
        try:
            with open(self.filename, "a") as file:
                np.savetxt(file, data, header=header, fmt=fmt)
        except AttributeError:
            print("Format has wrong shape. Numpy default format will be used")
            with open(self.filename, "a") as file:
                np.savetxt(file, data, header=header)


class Client:
    async def connect(self, interface: str, port: int) -> None:
        """Connect to a wavemeter server."""
        self.reader, self.writer = await asyncio.open_connection(interface, port)


    async def measure_cycle(
            self,
            filename: str,
            clients: [[str]],
            request: str,
            repetition: int=0,
            start_time: datetime=0,
            sleep_time: int=0,
            measure_time: int=0,
            additional_info: str=None
    ) -> None:
        """

        """
        file = MakeFile(filename, clients, additional_info=additional_info)
        file.set_repeat_count(repetition)
        file.set_repeat_measure_time(measure_time)
        file.set_repeat_sleep(sleep_time)

        while "program is running":
            if measure_time:  # check if there is a max measure time set, else continue
                active_time: timedelta = datetime.now() - file.time_started
                if active_time.microseconds >= measure_time:
                    break
            await self.requests_to_file(file, request)
            if repetition:
                repetition -= 1
                if not repetition:
                    break
            await asyncio.sleep(sleep_time)


    async def requests_to_file(self, file: MakeFile, request: str) -> None:
        """
        Measures the given requests and writes them down in a text file.

        Parameter
        ---------
        request: str
            Requests as scpi commands.
        """
        data = np.zeros(request.count("\n") + request.count(",") + 1)
        file.set_column_names(request)
        event_time: timedelta = datetime.now() - file.time_started
        data[0] = event_time.microseconds
        data[1:] = await self.request(request)

        file.write_txt_file([data])


    async def request(self, request: str) -> [Any]:
        """Called by user on client object."""
        await self.send_request(request)

        results = []
        for i in range(request.count("\n") + request.count(",")):
                answer = await self.receive_answer()
                results.append(answer)

        # while "receiving answers":
        #     answer = await self.receive_answer()
        #     results.append(answer)
        #     if not request:
        #         break

        return results


    async def send_request(self, request: str) -> None:
        """Send request into stream."""
        print(f"Send: {request!r}")
        self.writer.write(request.encode())
        await self.writer.drain()
        print("Writer drained.")

    async def receive_answer(self) -> Any:
        """Retrieve from stream."""
        data = await asyncio.wait_for(self.reader.readline(), timeout=2)
        data = data.decode().rstrip()
        print(f"Received: {data!r}")
        return data


    def __init__(self, interface: str, port: int):
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.interface: str | None = interface
        self.port: int = port

    async def __aenter__(self):
        await self.connect(self.interface, self.port)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Close the connection")
        self.writer.close()
        await self.writer.wait_closed()
        pass

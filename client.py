from __future__ import annotations

import asyncio
from datetime import datetime
import time
from typing import Any
import os

import numpy as np

# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection(
#         '127.0.0.1', 5555)
#
#     print(f'Send: {message!r}')
#     writer.write(message.encode())
#     await writer.drain()
#     print("Writer drained.")
#
#     # while "connected":
#     data = await reader.readline()  # TODO: Needs own loop or input/output worker, see above
#     data = data.decode().rstrip()
#     print(f'Received: {data!r}')
#         # if not data:
#         #     break
#
#     print('Close the connection')
#     writer.close()
#     await writer.wait_closed()
#
#
# asyncio.run(tcp_echo_client('MEAS:FREQ:CH? 1\n'))#MEASure:CHannel? 1\nMEASure:CHannel? 1\n\n'))


class MakeFile:

    standard_column_names = {
        "time": "t/s",
        "MEASure:WAVElength:CHannel": "CH:1/nm"
    }

    def __init__(self, filename: str, column_names: [str] | None=None):
        self.filename: str = filename
        self.time_connected: datetime = datetime.now()
        self.time_started: datetime | str = "not started"
        self.time_interval: datetime | int | str = "inf"  # can be repeating times, timeinterval or specified time (like a one time measurement at the morning)
        self.wavemeter_info: str = "no wavemeter info"

        if not self.filename[-4:] == ".txt":
            self.filename = self.filename + ".txt"
        if column_names:
            self.set_column_names(*column_names)
        else:
            self.column_names: str = "t/s   T/°C    CH:1/nm"
        self.set_time_started()

        self.time_info: str = (
                "Connected: " +
                str(self.time_connected) +
                "   Started: " +
                str(self.time_started) +
                "   Interval: " +
                str(self.time_interval) +
                "   Stopped: "
        )
        self.header: str = (
                self.time_info +
                "\n" +
                self.wavemeter_info +
                "\n\n" +
                self.column_names
        )

    def set_wavemeter_info(self, *wavemeter_info: str) -> None:
        for wm in wavemeter_info:
            self.wavemeter_info += str(wm)


    def set_column_names(self, column_names: str) -> None:
        if column_names:
            self.column_names = column_names

    def set_time_started(self, time_started: datetime | str | int | None=None) -> None:
        if time_started:
            self.time_started = str(time_started)
        else:
            self.time_started = datetime.now()


    def write_txt_file(self, data: [float], fmt: [str] | None=None, stopped_time: int| None=None) -> None:
        header: str = ""
        if not os.path.isfile(self.filename):
            header = self.header
        if fmt is None:
            fmt = ("%i", "%.3f", "%.8f", "%.8f", "%.8f", "%.8f")
        if stopped_time:
            self.time_info + str(stopped_time)
        try:
            with open(self.filename, "a") as file:
                np.savetxt(file, data, header=header, fmt=fmt)
        except AttributeError:
            print("Format has wrong shape. Numpy default format will be used")
            with open(self.filename, "a") as file:
                np.savetxt(file, data, header=header)


class Client:
    async def connect(self, interface: str, port: int) -> None:
        self.reader, self.writer = await asyncio.open_connection(interface, port)


    def set_filename(self, filename: str) -> None:
        """Sets the default filename where the measurement results will be saved."""
        self.filename = filename

    def set_header(self, header: str) -> None:
        """Sets the header for save files."""
        self.header = header


    async def requests_to_file(self, file: MakeFile, request: str) -> None:
        """
        Measures the given requests and writes them down in a text file.

        Parameter
        ---------
        request: str
            Requests as scpi commands.
        filename: str | None =None
            Name of file to save the data. If none is given the default will be used.
            If the default filename is None the user will be asked to give a filename via input.
        """
        data = np.zeros(request.count("\n") + request.count(",") + 1)
        event_time = datetime.now()
        data[0] = float(event_time.second)
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
        data = await self.reader.readline()
        data = data.decode().rstrip()
        # if not data:
        #     print("Channel not active.")
        #     data = "0.0"
        print(f"Received: {data!r}")

        return data

    def __init__(self, interface: str, port: int):
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.interface: str | None = interface
        self.port: int = port
        self.header = None

    async def __aenter__(self):
        await self.connect(self.interface, self.port)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Close the connection")
        self.writer.close()
        await self.writer.wait_closed()
        pass

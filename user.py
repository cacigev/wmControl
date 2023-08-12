#!/usr/bin/env python
from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any, Callable, Iterable, Sequence

import janus

# from bliss.comm.scpi import FuncCmd, ErrCmd, IntCmd, Commands
from decouple import config
from scpi import Commands

from wmControl.wavemeter import Wavemeter
from wmControl.wlmConst import DataPackage

dll_path = None
if sys.platform == "win32":
    dll_path = "./wmControl/wlmData.dll"
elif sys.platform == "linux":
    dll_path = "./wmControl/libwlmData.so"


def parse_log_level(log_level: int | str) -> int:
    """
    Parse an int or string, then return its standard log level definition.
    Parameters
    ----------
    log_level: int or str
        The log level. Either a string or a number.
    Returns
    -------
    int
        The log level as defined by the standard library. Returns logging.INFO as default
    """
    try:
        level = int(log_level)
    except ValueError:
        # parse the string
        level = logging.getLevelName(str(log_level).upper())
    if isinstance(level, int):
        return level
    return logging.INFO  # default log level


def create_scpi_commands(wavemeter: Wavemeter) -> None:  # Will move to init of wavemeter.
    """
    Creates for every wavemeter a dictionary of commands.

    Parameter
    ---------
    wavemeter: Wavemeter
        Device which receive commands.
    """
    # Config-file?
    wavemeter.commands = Commands(
        {
            # Mandatory commands.
            "*CLS": "Clear Status Command",
            "*ESE": "Standard Event Status Enable Command",
            "*ESR": "Standard Event Status Register Query",
            "*IDN": wavemeter.get_wavemeter_info(),
            "*OPC": "Operation Complete Command",
            "*RST": "Reset Command",  # No switcher mode active? Setting wavelength measurement to vacuum wavelength? ...
            "*SRE": "Service Request Enable Command",
            "*STB": "Read Status Byte Query",
            "*TST": "Self-Test Query",
            "*WAI": "Wait-to-Continue Command",
            # Device specific commands.
            "MEASure:SCALar:WAVElength:CHannel 1": wavemeter.get_wavelength(0),
            "MEASure:WAVElength:CHannel 1": wavemeter.get_wavelength(0),
            "MEASure:CHannel 1": wavemeter.get_wavelength(0),
            "MEASure:SCALar:WAVElength:CHannel 2": wavemeter.get_wavelength(1),
            "MEASure:WAVElength:CHannel 2": wavemeter.get_wavelength(1),
            "MEASure:CHannel 2": wavemeter.get_wavelength(1),
            "MEASure:SCALar:WAVElength:CHannel 3": wavemeter.get_wavelength(2),
            "MEASure:WAVElength:CHannel 3": wavemeter.get_wavelength(2),
            "MEASure:CHannel 3": wavemeter.get_wavelength(2),
            "MEASure:SCALar:WAVElength:CHannel 4": wavemeter.get_wavelength(3),
            "MEASure:WAVElength:CHannel 4": wavemeter.get_wavelength(3),
            "MEASure:CHannel 4": wavemeter.get_wavelength(3),
            "MEASure:SCALar:WAVElength:CHannel 5": wavemeter.get_wavelength(4),
            "MEASure:WAVElength:CHannel 5": wavemeter.get_wavelength(4),
            "MEASure:CHannel 5": wavemeter.get_wavelength(4),
            "MEASure:SCALar:WAVElength:CHannel 6": wavemeter.get_wavelength(5),
            "MEASure:WAVElength:CHannel 6": wavemeter.get_wavelength(5),
            "MEASure:CHannel 6": wavemeter.get_wavelength(5),
            "MEASure:SCALar:WAVElength:CHannel 7": wavemeter.get_wavelength(6),
            "MEASure:WAVElength:CHannel 7": wavemeter.get_wavelength(6),
            "MEASure:CHannel 7": wavemeter.get_wavelength(6),
            "MEASure:SCALar:WAVElength:CHannel 8": wavemeter.get_wavelength(7),
            "MEASure:WAVElength:CHannel 8": wavemeter.get_wavelength(7),
            "MEASure:CHannel 8": wavemeter.get_wavelength(7),
            "MEASure:SCALar:FREQuency:CHannel 1": wavemeter.get_frequency(0),
            "MEASure:FREQuency:CHannel 1": wavemeter.get_frequency(0),
            "MEASure:SCALar:FREQuency:CHannel 2": wavemeter.get_frequency(1),
            "MEASure:FREQuency:CHannel 2": wavemeter.get_frequency(1),
            "MEASure:SCALar:FREQuency:CHannel 3": wavemeter.get_frequency(2),
            "MEASure:FREQuency:CHannel 3": wavemeter.get_frequency(2),
            "MEASure:SCALar:FREQuency:CHannel 4": wavemeter.get_frequency(3),
            "MEASure:FREQuency:CHannel 4": wavemeter.get_frequency(3),
            "MEASure:SCALar:FREQuency:CHannel 5": wavemeter.get_frequency(4),
            "MEASure:FREQuency:CHannel 5": wavemeter.get_frequency(4),
            "MEASure:SCALar:FREQuency:CHannel 6": wavemeter.get_frequency(5),
            "MEASure:FREQuency:CHannel 6": wavemeter.get_frequency(5),
            "MEASure:SCALar:FREQuency:CHannel 7": wavemeter.get_frequency(6),
            "MEASure:FREQuency:CHannel 7": wavemeter.get_frequency(6),
            "MEASure:SCALar:FREQuency:CHannel 8": wavemeter.get_frequency(7),
            "MEASure:FREQuency:CHannel 8": wavemeter.get_frequency(7),
        }
    )


def decode_scpi(wavemeter: Wavemeter, message: str) -> Callable:
    # TODO: Must turn into a generator else "RuntimeError: cannot reuse already awaited coroutine"
    # Its disallowed to instantiate and await the same coroutine twice in a row.
    # Maybe replacing with futures.
    # See also https://bugs.python.org/issue25887
    """
    Decoder of scpi orders.

    Parameter
    ---------
    message : str
        Message to decode.
    """
    command = wavemeter.commands[message]

    return command


async def read_stream(wavemeter: Wavemeter, reader: asyncio.StreamReader, requests: janus.AsyncQueue[Callable]) -> None:
    """
    Reads input from client out of stream.

    Parameter
    ---------
    reader: asyncio.StreamReader
        Reader of client connection.
    requests: janus.AsyncQueue
        Queue receiving requests from stream.
    """
    while "Connection open":
        # Read next line in stream.
        request: bytes = await reader.readline()
        message: str = request.decode().rstrip()
        print(f"Read: {message}")
        if not message:
            break

        try:
            # Decode SCPI request.
            command: Callable = decode_scpi(wavemeter, message)
            # Put the request into the request queue.
            await requests.put(command)
        except KeyError:
            logging.getLogger(__name__).info("Received unknown command.")
            # await requests.put('Received unknown command.')
            # TODO: Add error to register.


async def listen_wm(client_requests: janus.AsyncQueue[Callable], measurements: janus.AsyncQueue[DataPackage]) -> None:
    """
    Puts asked measurement results of a wavemeter into a queue.

    Parameter
    ---------
    wavemeter: Wavemeter
        Device the server listens.
    client_requests: janus.AsyncQueue
        Requests from clients.
    measurements: janus.AsyncQueue
        Results from wavemeter.
    """
    request = await client_requests.get()

    print(f"Request: {request}")
    result = await request
    print(f"Result: {result}")
    await measurements.put(result)


async def write_stream(writer: asyncio.StreamWriter, measurements: janus.AsyncQueue[DataPackage]) -> None:
    """
    Writes the results into the stream.

    Parameter
    ---------
    writer: asyncio.StreamWriter
        Writer of client connection.
    measurements: janus.AsyncQueue
        Queue holding the results.
    """
    print("Writing.")
    result = await measurements.get()

    print(f"Send: {result!r}")
    writer.write(str(result).encode())
    print("Message send. Draining writer.")
    await writer.drain()
    print("Writer drained.")


async def create_wm_server(product_id: int, host: str, port: int) -> None:
    """
    Creates a server for every connected wavemeter.

    The handling for client requests is enclosed.

    Parameter
    ---------
    product_id: int
        Version of the WM. Works like a serial number just not named like it.
    host: str
        IP-address of host.
    port: int
        Port-number to call and listen for a wavemeter. Specified through product_id.
    """

    async def handle_request(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Handles client requests. Everytime called if a client connects to the server.

        Parameter
        ---------
        reader : asyncio.StreamReader
            Reader of the client.
        writer : asyncio.StreamWriter
            Writer of the client.
        """
        print("Got request.")
        client_requests: janus.Queue[str] = janus.Queue()  # Queue which gathers client requests.
        measurements: janus.Queue[Any] = janus.Queue()  # Queue with answers for client.
        tasks: set[asyncio.Task] = set()  # Set with TODOs.

        # Received requests.
        # Read input from client.
        ask = asyncio.create_task(read_stream(wavemeter, reader, client_requests.async_q))
        tasks.add(ask)

        # Listen for answers from wavemeter.
        answer = asyncio.create_task(listen_wm(client_requests.async_q, measurements.async_q))
        tasks.add(answer)

        # Publish answers.
        publish = asyncio.create_task(write_stream(writer, measurements.async_q))
        tasks.add(publish)

        await asyncio.gather(*tasks)  # Gather tasks and wait for them to be done.
        print("Tasks done.")

        # Closing the connection.
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async with Wavemeter(product_id, dll_path=dll_path) as wavemeter:  # Activate wavemeter.
        create_scpi_commands(wavemeter)
        server = await asyncio.start_server(handle_request, host, port)
        address = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {address}")

        async with server:
            await server.serve_forever()


async def main(wavemeter_config: Iterable[tuple[int, tuple[str | Sequence[str] | None, int]]]):
    server_list: set[asyncio.Task] = set()
    for wavemeter_id, (interface, port) in wavemeter_config:
        server = asyncio.create_task(create_wm_server(wavemeter_id, interface, port))
        server_list.add(server)

    await asyncio.gather(*server_list)


logging.basicConfig(
    # format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    format="%(message)s",
    level=config("APPLICATION_LOG_LEVEL", default=logging.INFO, cast=parse_log_level),
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    # 4711: Quips B 192.168.1.240
    # 536: WS-6
    wm_list = [(4734, ("127.0.0.1", 5555)), (536, ("127.0.0.1", 5556))]
    asyncio.run(main(wm_list))
except KeyboardInterrupt:
    pass
finally:
    logging.getLogger(__name__).info("Application shut down.")

#!/usr/bin/env python
from __future__ import annotations

import asyncio
import logging
import sys

from typing import Any, Callable
# from bliss.comm.scpi import FuncCmd, ErrCmd, IntCmd, Commands
from decouple import config
import janus
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
    wavemeter.commands = Commands({
        '*IDN': wavemeter.get_wavemeter_info(),
        '*RST': 'resetting device',  # No switcher mode active? Setting wavelength measurement to vacuum wavelength? ...
        '*CLS': 'clear status',  # ?
        '*READ': wavemeter.get_wavelength(0),
        'test': 'test'
         }
    )
    print(wavemeter.commands['test'])


def decode_scpi(wavemeter: Wavemeter, message: str) -> Callable:
    """
    Decoder of scpi orders.

    Parameter
    ---------
    message : str
        Message to decode.
    """
    try:
        command = wavemeter.commands[message]
        return command
    except NameError:
        logging.getLogger(__name__).info('Received unknown command.')
        raise


async def read_stream(
        wavemeter: Wavemeter,
        reader: asyncio.StreamReader,
        requests: janus.AsyncQueue[Callable]
) -> None:
    """
    Reads input from client out of stream.

    Parameter
    ---------
    reader: asyncio.StreamReader
        Reader of client connection.
    requests: janus.AsyncQueue
        Queue receiving requests from stream.
    """
    # while "Connection open":
    # Read next line in stream.
    request: bytes = await reader.readline()
    message: str = request.decode().rstrip()
    print(f"Read: {message}")
    # if not message:
    #     break

    # Decode SCPI request.
    command: Callable = decode_scpi(wavemeter, message)
    # Put the request into the request queue.
    await requests.put(command)



async def listen_wm(
        client_requests: janus.AsyncQueue[Callable],
        measurements: janus.AsyncQueue[DataPackage]
) -> None:
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


async def write_stream(
        writer: asyncio.StreamWriter,
        measurements: janus.AsyncQueue[DataPackage]
) -> None:
    """
    Writes the results into the stream.

    Parameter
    ---------
    writer: asyncio.StreamWriter
        Writer of client connection.
    measurements: janus.AsyncQueue
        Queue holding the results.
    """
    print('Writing.')
    result = await measurements.get()

    print(f"Send: {result!r}")
    writer.write(str(result).encode())
    await writer.drain()


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
        print('Got request.')
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

        try:
            await asyncio.gather(*tasks, return_exceptions=True)  # Gather tasks and wait for them to be done.
            print('Tasks done.')
        except Exception:
            raise

        # Closing the connection.
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async with Wavemeter(product_id, dll_path=dll_path) as wavemeter:  # Activate wavemeter.
        create_scpi_commands(wavemeter)
        server = await asyncio.start_server(
            handle_request, host, port)
        address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {address}')

        async with server:
            await server.serve_forever()


async def main(wavemeter: [(int, int)]):
    server_list: set[asyncio.Task] = set()
    for wm, port in wavemeter:
        server = asyncio.create_task(create_wm_server(wm, '127.0.0.1', port))
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
    wm_list = [(4734, 5555), (536, 5556)]
    asyncio.run(main(wm_list))
except KeyboardInterrupt:
    pass
finally:
    logging.getLogger(__name__).info("Application shut down.")

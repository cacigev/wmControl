#!/usr/bin/env python
from __future__ import annotations

import asyncio
import logging
import sys

from typing import Any
# from bliss.comm.scpi import FuncCmd, ErrCmd, IntCmd, Commands
from decouple import config
import janus

from wmControl.wavemeter import Wavemeter


dll_path = None
commands = None
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


def create_scpi_commands():
    # commands = Commands({'*CLS': FuncCmd(doc='clear status'),
    #                      '*RST': FuncCmd(doc='reset')
    #                      })
    #     c2 = Commands(c1, VOLTage=IntCmd()))
    pass


async def decode_scpi(message: str):
    """
    Decoder of scpi orders.

    Parameter
    ---------
    message : str
        Message to decode.
    """

    pass


async def read_stream(reader: asyncio.StreamReader, requests: janus.AsyncQueue):
    """
    Reads input from client out of stream.

    Parameter
    ---------
    reader: asyncio.StreamReader
        Reader of client connection.
    requests: janus.AsyncQueue
        Queue receiving requests from stream.
    """
    # Read next line in stream.
    request = await reader.readline()
    message = request.decode().rstrip()
    # Decode SCPI request.
    # message = await decode_scpi(message)

    print(f"Read: {message}")
    await requests.put(message)


async def listen_wm(wavemeter: Wavemeter, client_requests: janus.AsyncQueue, measurements: janus.AsyncQueue) -> None:
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
    # wavemeter.request(*args) instead of wavemeter.get_wavelength(0)

    print(f"Request: {request}")
    result = await wavemeter.get_wavelength(0)
    print(f"Result: {result}")
    await measurements.put(result)


async def write_stream(writer: asyncio.StreamWriter, measurements: janus.AsyncQueue):
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
        ask = asyncio.create_task(read_stream(reader, client_requests.async_q))
        tasks.add(ask)

        # Create new WM-object to answer the request.
        answer = asyncio.create_task(listen_wm(wavemeter, client_requests.async_q, measurements.async_q))
        tasks.add(answer)

        # Publish answers
        publish = asyncio.create_task(write_stream(writer, measurements.async_q))
        tasks.add(publish)

        await asyncio.gather(*tasks)  # Gather tasks and wait for them to be done.
        print('Tasks done.')

        # Closing the connection.
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async with Wavemeter(product_id, dll_path=dll_path) as wavemeter:  # Activate wavemeter.
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

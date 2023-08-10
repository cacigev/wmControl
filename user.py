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

    pass


async def create_wm_server(product_id: int, host: str, port: int) -> asyncio.Server:
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
        client_requests: janus.Queue[str] = janus.Queue()  # Queue which gathers client requests.
        measurements: janus.Queue[Any] = janus.Queue()  # Queue with answers for client.
        tasks: set[asyncio.Task] = set()  # Set with TODOs.
        # Received requests.
        # ...
        # read out stream from client

            # Decode SCPI request.
            # coro = await decode_scpi(message)

        # Create new WM-object to answer the request.
        # ...
        # listen for answers
        # get request with client_requests.get()
        # put answer in measurements.put()

        # Scream answers
        # ...
        # measurements.get() to stream with write
        print(f"Send: {measurement!r}")
        writer.write(str(measurement).encode())
        await writer.drain()

        await asyncio.gather(*tasks)  # Gather tasks and wait for them to be done.

        # Closing the connection.
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(
        handle_request, host, port)
    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {address}')

    async with server:
        await server.serve_forever()

    return server


async def main(wavemeter: [(int, int)]):
    server_list: set[asyncio.Server] = set()
    for wm, port in wavemeter:
        server = await create_wm_server(wm, '127.0.0.1', port)

        server_list.add(server)

    await asyncio.gather(*server_list)


    # async with server:
    #     await server.serve_forever()


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

#!/usr/bin/env python
from __future__ import annotations

import asyncio
import logging
import sys

from bliss.comm.scpi import FuncCmd, ErrCmd, IntCmd, Commands
from decouple import config

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
    print('')
    # Received requests.
    while "EOF not reached":
        data = await reader.readline()
        if not data:  # <---------
            break

        message = data.decode().rstrip()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

        # Decode SCPI request.
        coro = await decode_scpi(message)

        # Create new WM-object to answer the request.
        # 4711: Quips B 192.168.1.240
        # 536: WS-6
        async with Wavemeter(4734, dll_path=dll_path) as ws8, Wavemeter(536, dll_path=dll_path) as ws6:
            measurement = await ws8.get_wavelength(0)

        print(f"Send: {measurement!r}")
        writer.write(str(measurement).encode())
        await writer.drain()

    # Closing the connection.
    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_request, '127.0.0.1', 8888)

    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {address}')

    async with server:
        await server.serve_forever()


logging.basicConfig(
    # format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    format="%(message)s",
    level=config("APPLICATION_LOG_LEVEL", default=logging.INFO, cast=parse_log_level),
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.getLogger(__name__).info("Application shut down.")

#!/usr/bin/env python
from __future__ import annotations

import asyncio
import logging
import sys
from functools import partial
from typing import Any, Callable, Coroutine, Iterable, Sequence

from decouple import config
from scpi import Commands, split_line

from wmControl.wavemeter import Wavemeter

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


def create_scpi_protocol(wavemeter: Wavemeter) -> Commands:
    """
    Creates for every wavemeter a dictionary of commands.

    Parameter
    ---------
    wavemeter: Wavemeter
        Device which receive commands.
    """
    return Commands(
        {
            # Mandatory commands.
            "*CLS": "Clear Status Command",
            "*ESE": "Standard Event Status Enable Command",
            "*ESR": "Standard Event Status Register Query",
            "*IDN": partial(wavemeter.get_wavemeter_info),  # No partial required, because there are no parameters
            "*OPC": "Operation Complete Command",
            "*RST": "Reset Command",  # No switcher mode active? Setting wavelength measurement to vacuum wavelength? ...
            "*SRE": "Service Request Enable Command",
            "*STB": "Read Status Byte Query",
            "*TST": "Self-Test Query",
            "*WAI": "Wait-to-Continue Command",
            # Device specific commands.
            "MEASure:WAVElength:CHannel": partial(wavemeter.get_wavelength),  # wavelength of specific channel
            "MEASure:WAVElength": partial(wavemeter.get_wavelength),  # all wavelengths
            # Note for thesis: Calling wavelength and right after frequency leads to two different measurements.
            "MEASure:FREQuency:CHannel": partial(wavemeter.get_frequency),
            "MEASure:FREQuency": partial(wavemeter.get_frequency),
            "MEASure:TEMPerature": partial(wavemeter.get_temperature),
        }
    )


async def read_stream(reader: asyncio.StreamReader, job_queue: asyncio.Queue[bytes]) -> None:
    """
    Reads input from client out of stream.

    Parameter
    ---------
    reader: asyncio.StreamReader
        Reader of client connection.
    requests: janus.AsyncQueue
        Queue receiving requests from stream.
    """
    while "processing commands":
        # Commands are separated by a newline
        request = await reader.readline()
        logging.getLogger(__name__).debug("Received '%s' from client.", request)
        await job_queue.put(request)


async def write_stream(
    writer: asyncio.StreamWriter, protocol: Commands, job_queue: asyncio.Queue[bytes], device_timeout: float
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
    while "sending replies":
        request = await job_queue.get()
        try:
            request_str = request.decode().rstrip()
        except UnicodeDecodeError:
            continue  # TODO: reply with an error

        # Try to decode SCPI request.
        try:
            scpi_requests = split_line(request_str)
        except KeyError:
            logging.getLogger(__name__).info("Received unknown request: '%s'.", request_str)
            continue
            # await requests.put('Received unknown command.')
            # TODO: reply with an error

        for scpi_request in scpi_requests:
            try:
                parsed_command = protocol[scpi_request.name]
            except KeyError:
                # TODO: return an error
                logging.getLogger(__name__).info("Unknown request received: '%s'.", scpi_requests)
                break
            try:
                result = await asyncio.wait_for(parsed_command(int(scpi_request.args)), timeout=device_timeout)
                # TODO: Duck typing of args or parsing to correct type in wlmData
                if scpi_request.query:
                    print(f"Send: {result!r}")
                    # Results are separated by a newline.
                    writer.write((str(result) + "\n").encode())
                    print("Message send. Draining writer.")
                    await writer.drain()
                    print("Writer drained.")
            except TimeoutError:
                logging.getLogger(__name__).debug("Timeout error querying the wavemeter.")


def create_client_handler(
    wavemeter: Wavemeter,
) -> Callable[[asyncio.StreamReader, asyncio.StreamWriter], Coroutine[Any, Any, None]]:
    """
    A closure to inject the wavemeter into the client callback handler.

    Parameters
    ----------
    wavemeter: Wavemeter
        The wavemeter managed by this handler

    Returns
    -------
    Coroutine
        The client_connected_cb callback that can be passed to asyncio.start_server().
    """

    async def client_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        The client handler exclusively serves a single client and passes the commands to the wavemeter while returning
        the results to the client. The input (reader) and output (writer) is separated by a queue to minimize any
        lag introduced by delays with the wavemeter communication.

        Parameter
        ---------
        reader : asyncio.StreamReader
            Handles the incoming traffic.
        writer : asyncio.StreamWriter
            Pushes the outbound traffic to the client.
        """
        # Limit the size of the job queue to create backpressure on the input
        job_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=5)
        tasks: set[asyncio.Task] = set()  # Set with TODOs.

        # Read the inputs from the client
        input_task = asyncio.create_task(read_stream(reader, job_queue=job_queue))
        tasks.add(input_task)

        # Execute commands and send back the results
        protocol = create_scpi_protocol(wavemeter)
        publish = asyncio.create_task(write_stream(writer, protocol, job_queue, device_timeout=2.0))
        tasks.add(publish)

        await asyncio.gather(*tasks)  # Gather tasks and wait for them to be done.
        print("Tasks done.")

        # Closing the connection.
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    return client_handler


async def create_wm_server(product_id: int, interface: str | Sequence[str] | None, port: int) -> None:
    """
    Create a wavemeter SCPI server. The server listens at the given port and passes the commands to the wavemeter with
    the given product_id.

    Parameter
    ---------
    product_id: int
        Version of the WM. Works like a serial number just not named like it.
    interface: str or Sequence[str] or None
        The interface to listen on. If a str is given, the server is bound to that interface. If a sequence is given,
        the server is bound to the interfaces given. If set to None, the server is bound to all available interfaces.
    port: int
        The port number to listen at.
    """
    assert isinstance(port, int) and port > 0
    async with Wavemeter(product_id, dll_path=dll_path) as wavemeter:  # Activate wavemeter.
        server = await asyncio.start_server(
            client_connected_cb=create_client_handler(wavemeter), host=interface, port=port
        )

        async with server:
            logging.getLogger(__name__).info("Serving wavemeter %i on %s:%i", wavemeter.product_id, interface, port)
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

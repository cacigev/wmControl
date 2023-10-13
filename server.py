#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any, Callable, Coroutine, Iterable, Sequence

from decouple import UndefinedValueError, config
from pydantic import IPvAnyInterface, ValidationError
from scpi import Commands, split_line

from _version import __version__
from config_parser import parse_log_level, parse_wavemeter_config
from scpi_protocol import ScpiException, UnexpectedNumberOfParameterException, create_scpi_protocol
from wmControl.wavemeter import Wavemeter
from wmControl.wlmConst import NoWavemeterAvailable

dll_path = None
if sys.platform == "win32":
    if config("CONNECTION_TYPE", default="REMOTE") == "LOCAL":
        dll_path = "C:/Windows/System32/wlmData.dll"
    else:
        dll_path = "./wmControl/wlmData.dll"
elif sys.platform == "linux":
    if config("CONNECTION_TYPE", default="REMOTE") == "LOCAL":
        raise ValueError("Cannot connect locally using Linux.")
    dll_path = "./wmControl/libwlmData.so"


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
    request: bytes
    async for request in reader:
        # Commands are separated by a newline
        if not request:
            # The client closed the connection
            break
        logging.getLogger(__name__).debug("Received '%s' from client.", request)
        await job_queue.put(request)


async def write_stream(
    writer: asyncio.StreamWriter, protocol: Commands, job_queue: asyncio.Queue[bytes], device_timeout: float
) -> None:
    """
    Parses the SCPI request and replies if needed. This is the main worker, because it parses the SCPI request and does
    the error handling.

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
                # TODO: reply with an error
                logging.getLogger(__name__).info("Unknown request received: '%s'.", scpi_requests)
                break
            logging.getLogger(__name__).debug("Received SCPI request: %s", parsed_command.get("doc", parsed_command))
            try:
                function_call = parsed_command["get" if scpi_request.query else "set"]
            except KeyError:
                # TODO: reply with an error
                continue
            result: str

            try:
                try:
                    if scpi_request.args:
                        coro = function_call(parsed_command["decode"](scpi_request.args))
                    else:
                        coro = function_call()
                except TypeError:
                    raise UnexpectedNumberOfParameterException from None
                result = await coro
            except ScpiException as exc:
                # Return a SCPI error
                writer.write(f"{exc}\n".encode())
                continue
            except TimeoutError:
                logging.getLogger(__name__).debug("Timeout error while querying the wavemeter. Dropping request.")
                break

            if scpi_request.query:
                writer.write((parsed_command["encode"](result) + "\n").encode())
                await writer.drain()


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
    Callable
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
        pending_tasks: set[asyncio.Task] = set()  # Set with TODOs.

        # Read the inputs from the client
        input_task = asyncio.create_task(read_stream(reader, job_queue=job_queue))
        pending_tasks.add(input_task)

        # Execute commands and send back the results
        protocol = create_scpi_protocol(wavemeter)
        publish = asyncio.create_task(write_stream(writer, protocol, job_queue, device_timeout=2.0))
        pending_tasks.add(publish)

        try:
            while pending_tasks:
                done: set[asyncio.Task]
                done, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
                for completed_task in done:
                    try:
                        task_exc = completed_task.exception()  # Raises a CancelledError if the task has been cancelled
                    except asyncio.exceptions.CancelledError:
                        # If the task was canceled, there is no further action needed.
                        continue
                    if task_exc is not None:
                        # An exception was raised. Terminate now.
                        logging.getLogger(__name__).error("Error while serving client.", exc_info=task_exc)
                    for pending_task in pending_tasks:
                        pending_task.cancel()
                    try:
                        await asyncio.gather(*pending_tasks)
                    except asyncio.CancelledError:
                        pass
        finally:
            logging.getLogger(__name__).debug("Shutting down client handler.")
            # Cancel all remaining tasks
            for pending_task in pending_tasks:
                pending_task.cancel()
            try:
                await asyncio.gather(*pending_tasks)
            except asyncio.CancelledError:
                pass
            finally:
                try:
                    await writer.drain()
                    writer.close()
                    await asyncio.wait_for(writer.wait_closed(), timeout=1.0)
                except OSError:
                    # Catches TimeoutErrors (from wait_for) and ConnectionErrors (from writer.drain())
                    pass

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
            logging.getLogger(__name__).info(
                "Serving wavemeter %i on %s",
                wavemeter.product_id,
                ", ".join(f"{sock.getsockname()[0]}:{sock.getsockname()[1]}" for sock in server.sockets),
            )
            await server.serve_forever()


async def main(wavemeter_config: Iterable[tuple[int, IPvAnyInterface | Sequence[IPvAnyInterface] | None, int]]):
    server_list: set[asyncio.Task] = set()
    wavemeters_configured: set[int] = set()

    logging.getLogger(__name__).warning("#################################################")
    logging.getLogger(__name__).warning("Starting SCPI daemon v%s...", __version__)
    logging.getLogger(__name__).warning("#################################################")

    for wavemeter_id, interface, port in wavemeter_config:
        if interface is not None:
            try:
                interface_str = [str(iface.ip for iface in interface)]
            except TypeError:
                # Not an iterable
                interface_str = str(interface.ip)
        else:
            interface_str = None

        server = asyncio.create_task(create_wm_server(wavemeter_id, interface_str, port))
        server_list.add(server)
        wavemeters_configured.add(wavemeter_id)

    logging.getLogger(__name__).info("Wavemeter configurations found for %s...", wavemeters_configured)
    await asyncio.gather(*server_list)


logging.basicConfig(
    # format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    format="%(message)s",
    level=config("APPLICATION_LOG_LEVEL", default=logging.INFO, cast=parse_log_level),
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 536: Quips B WS-6 192.168.1.240
# 4711: Quips B WS-8 192.168.1.240
# 4734: Quips C WS-8 192.168.1.45
try:
    wavemeters = parse_wavemeter_config(config("WAVEMETERS"))
except UndefinedValueError:
    logging.getLogger(__name__).error("No wavemeters defined. Check the 'WAVEMETERS' environment variable.")
except ValidationError as validation_exc:
    logging.getLogger(__name__).error(f"Invalid wavemeter configuration: {validation_exc}")
else:
    try:
        asyncio.run(main(wavemeters))
    except KeyboardInterrupt:
        pass
    finally:
        logging.getLogger(__name__).warning("#################################################")
        logging.getLogger(__name__).warning("Stopping SCPI daemon...")
        logging.getLogger(__name__).warning("#################################################")

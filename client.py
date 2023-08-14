import asyncio

import janus


# async def write_input(request: str) -> None:
#     """Called by user."""
#     async def __write_input(request_queue: janus.AsyncQueue) -> None:
#         """Put user input into queue."""
#         await request_queue.put(request)
#
#     await __write_input(request)
#
#
# async def write_stream(
#         writer: asyncio.StreamWriter,
#         request_queue: janus.AsyncQueue
# ) -> None:
#     """Sending commands to server."""
#     while "sending commands":
#         message = await request_queue.get()
#
#         if not message:
#             print('Close the connection')
#             writer.close()
#             await writer.wait_closed()
#             break
#         else:
#             print(f'Send: {message!r}')
#             writer.write(message.encode())
#             await writer.drain()
#             print("Writer drained.")
#
#
# async def read_stream(reader: asyncio.StreamReader):
#     """Receiving results from server."""
#     while "receiving results":
#         data = await reader.readline()
#         print(f'Received: {data.decode().rstrip()!r}')
#
#
# async def main():
#     reader, writer = await asyncio.open_connection('127.0.0.1', 5555)
#     request_queue: janus.Queue = janus.Queue()
#     tasks: set[asyncio.Task] = set()
#
#     user_input = asyncio.create_task(write_input(request_queue.async_q))
#     tasks.add(user_input)
#
#     stream_input = asyncio.create_task(write_stream(writer, request_queue.async_q))
#     tasks.add(stream_input)
#
#     publish = asyncio.create_task(read_stream(reader))
#     tasks.add(publish)
#
#     await asyncio.gather(*tasks)
#
#
# asyncio.run(main())


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 5555)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()
    print("Writer drained.")

    while "connected":
        data = await reader.readline()  # TODO: Needs own loop or input/output worker, see above
        data = data.decode().rstrip()
        print(f'Received: {data!r}')
        if not data:
            break

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_echo_client('MEAS:FREQ:CH? 1\n'))#MEASure:CHannel? 1\nMEASure:CHannel? 1\n\n'))

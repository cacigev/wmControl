import asyncio


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


class Client:

    async def connect(self, interface: str, port: int) -> None:
        self.reader, self.writer = await asyncio.open_connection(interface, port)


    async def request(self, request: str) -> None:
        """Called by user on client object."""
        await self.send_request(request)
        await self.receive_answer()
        pass


    async def send_request(self, request: str) -> None:
        """Send request into stream."""
        print(f'Send: {request!r}')
        self.writer.write(request.encode())
        await self.writer.drain()
        print("Writer drained.")

    async def receive_answer(self):
        """Retrieve from stream."""
        print('here')
        data = await self.reader.readline()
        data = data.decode().rstrip()
        print(f'Received: {data!r}')


    def __init__(self, interface: str, port: int):
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.interface: str | None = interface
        self.port: int = port


    async def __aenter__(self):
        await self.connect(self.interface, self.port)
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('Close the connection')
        self.writer.close()
        await self.writer.wait_closed()
        pass

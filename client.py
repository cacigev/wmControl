import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 5555)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.readline()
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('MEAS:WAVE:CH 1\n'))#*IDN\nMEASURE:WAVELENGTH:CHANNEL 1\n'))#Hello world!\n:CONTrol:EBENch:CLEan:INITiate\n'))

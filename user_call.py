"""
Template for an actual user file.
"""
import asyncio

import client
from client import Client


async def main():  # TODO: Dropping async-with-as and replacing through something like line 20/21
    async with Client('127.0.0.1', 5555) as wm_client:
        print(wm_client)
        await wm_client.send_request('MEAS:FREQ:CH? 1\nMEAS:FREQ:CH? 1\n')
        await wm_client.receive_answer()
        await wm_client.receive_answer()
        # await wm_client.request('MEAS:WAVE:CH 1\n')  # Manages both request and answer.

asyncio.run(main())

# wm = Client('127.0.0.1', 5555)
# measurement = wm.request('MEAS:WAVE:CH 1\nMEAS:FREQ:CH? 1\n')

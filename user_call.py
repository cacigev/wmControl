"""
Template for an actual user file.
"""
import asyncio
from decimal import Decimal
import os
import time

import numpy as np

import client
from client import Client, MakeFile


# name = "test_measurement_long_term_1.txt"

def write(filename: str, data: [Decimal]) -> None:
    header: str = ""
    if not os.path.isfile(filename):
        header = "date measurement\n"\
                 "started=time interval=seconds\n"\
                 "\n"\
                 "T/s TEMP/°C WAVE:CH:4/nm(vac) WaveCH:5/nm(vac) WaveCH:7/nm(vac)"
    with open(filename, "a") as file:
        np.savetxt(file, data, header=header, fmt=("%i", "%.3f", "%.8f", "%.8f", "%.8f", "%.8f"))

async def main():  # TODO: Dropping async-with-as and replacing through something like line 20/21
    async with Client('127.0.0.1', 5555) as wm_client, Client('127.0.0.1', 5556) as wm_client_2:
        print(wm_client)
        wm_info_1 = await wm_client.request("*IDN?\n")
        wm_info_2 = await wm_client_2.request("*IDN?\n")
        wm_info = [wm_info_1, wm_info_2]
        data = np.zeros(6)
        name = input("Filename: ")
        name = name + ".txt"
        file = MakeFile(name)
        for i in range(5):
            # await wm_client.send_request("GET:CH?\nGET:CH:COUNT?\n")

            # results = await wm_client.request("MEAS:TEMP?\nMEAS:FREQ:CH? 0,1,3,4\n")  # Manages both request and answer.
            # data[0] = (time.time())
            # data[1:] = results

            # Write data to file, wait and repeat.
            # write(name, [data])
            # file.write_txt_file([data])
            await wm_client.requests_to_file(file, "MEAS:TEMP?\nMEAS:FREQ:CH? 0,1,3,4\n")
            await asyncio.sleep(1)


asyncio.run(main())

# wm = Client('127.0.0.1', 5555)
# measurement = wm.request('MEAS:WAVE:CH 1\nMEAS:FREQ:CH? 1\n')

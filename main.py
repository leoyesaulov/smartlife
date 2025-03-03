import asyncio
from asyncio import sleep
from datetime import datetime

import light_switch

async def run():
    while True:
        light_switch.check()
        print("I ran at: " + datetime.now().strftime("%d.%b.%Y %H:%M:%S"))
        await sleep(600)

asyncio.run(run())
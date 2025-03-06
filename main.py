import asyncio
import threading
from asyncio import sleep
from datetime import datetime

import light_switch

async def run():
    while True:
        light_switch.check()
        print("I ran at: " + datetime.now().strftime("%d.%b.%Y %H:%M:%S"))
        await sleep(600)

async def listen_to_input():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "")
        input_arr = user_input.lower().split()
        match input_arr[0]:
            case "on":
                light_switch.on(int(input_arr[1]) if len(input_arr) > 1 else 25)
            case "off":
                light_switch.off()

async def main():
    await asyncio.gather(run(), listen_to_input())


asyncio.run(main())
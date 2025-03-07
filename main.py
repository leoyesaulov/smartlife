import asyncio
from asyncio import sleep
from datetime import datetime
import light_switch


event = asyncio.Event()
semaphore = 0
lock = asyncio.Lock()

async def run():
    while True:
        await event.wait()
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
                match len(input_arr):
                    case 1:
                        light_switch.on()
                    case 2:
                        light_switch.on(int(input_arr[1]))
                    case 3:
                        light_switch.on(int(input_arr[1]))
                        asyncio.create_task(wait(int(input_arr[1]) * 60))
            case "off":
                match len(input_arr):
                    case 1:
                        light_switch.off()
                    case 2:
                        light_switch.off()
                        asyncio.create_task(wait(int(input_arr[1]) * 60))
            case "timer":
                asyncio.create_task(wait(int(input_arr[1]) * 60))

async def wait(seconds):
    enter()
    await asyncio.sleep(seconds)
    release()

def enter():
    global semaphore
    async with lock:
        semaphore += 1
    event.clear()

def release():
    global semaphore
    async with lock:
        semaphore -= 1
        if semaphore <= 0:
            event.set()


async def main():
    event.set()
    await asyncio.gather(run(), listen_to_input())

asyncio.run(main())
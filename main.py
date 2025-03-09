import asyncio
from asyncio import sleep
from datetime import datetime
import light_switch


event = asyncio.Event()
semaphore = 0
lock = asyncio.Lock()
extra_tasks = []

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
                        print("waiting", input_arr[2], "minutes, starting at", datetime.now().strftime("%H:%M:%S"))
                        extra_tasks.append(asyncio.create_task(wait(int(input_arr[1]) * 60)))

            case "off":
                match len(input_arr):
                    case 1:
                        light_switch.off()
                    case 2:
                        light_switch.off()
                        extra_tasks.append(asyncio.create_task(wait(int(input_arr[1]) * 60)))
            case "timer":
                extra_tasks.append(asyncio.create_task(wait(int(input_arr[1]) * 60)))
            case "stop":
                await kill()


async def wait(seconds):
    await enter()
    await asyncio.sleep(seconds)
    print("wait complete at", datetime.now().strftime("%H:%M:%S"))
    await release()

async def enter():
    global semaphore
    async with lock:
        semaphore += 1
    event.clear()

async def release():
    global semaphore
    async with lock:
        semaphore -= 1
        if semaphore <= 0:
            event.set()

async def kill():
    global extra_tasks
    global semaphore
    async with lock:
        for task in extra_tasks:
            task.cancel()
        semaphore = 0
        event.set()

async def main():
    event.set()
    await asyncio.gather(run(), listen_to_input())

asyncio.run(main())
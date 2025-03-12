import asyncio
import logger
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
        logger.logInfo(f"Automated check has been performed.")
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
                        logger.logInfo(f"Timer of {input_arr[2]} minutes has been set.")
                        extra_tasks.append(asyncio.create_task(wait(int(input_arr[2]) * 60)))

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
            case _:
                print("I'm sorry, I didn't understand that.")


async def wait(seconds):
    await enter()
    await asyncio.sleep(seconds)
    logger.logInfo(f"Wait complete." )
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.logCritical(f"Critical error: {e=}" )
    finally:
        logger.logFatal("Terminating...")
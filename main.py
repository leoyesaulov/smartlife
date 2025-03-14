import asyncio
import os
import sys

from dotenv import load_dotenv
import logger
from asyncio import sleep
import light_switch


event = asyncio.Event()
semaphore = 0
lock = asyncio.Lock()
extra_tasks = []
load_dotenv()
cololight_strip = light_switch.LightStrip(ip=os.getenv("STRIP_IP"))

async def run():
    while True:
        await event.wait()
        cololight_strip.check()
        logger.logInfo(f"Automated check has been performed.")
        await sleep(600)
        
def parse(arr):
    out = {
        "mode": arr[0],
        "amount": 25 if arr[0] == 'on' and arr[1] == 0 else arr[1],
        "timer": arr[2]
    }
    return out

async def listen_to_input():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "")
        input_arr = user_input.lower().split()

        # padding the list
        input_arr = input_arr + [0]*(3-len(input_arr))
        
        input_dict = parse(input_arr)    
        
        mode = input_dict['mode']
        amount = input_dict['amount']
        timer = input_dict['timer']
      
        if mode == "on":
            cololight_strip.on(int(amount))
            
            if timer:
                logger.logInfo(f"Timer of {timer} minutes has been set.")
                extra_tasks.append(asyncio.create_task(wait(int(timer) * 60)))
            
            continue

        if mode == "off":
            cololight_strip.off()
            
            if timer:
                logger.logInfo(f"Timer of {timer} minutes has been set.")
                extra_tasks.append(asyncio.create_task(wait(int(timer) * 60)))
            continue

        if mode == "timer":
            logger.logInfo(f"Timer of {timer} minutes has been set.")
            extra_tasks.append(asyncio.create_task(wait(int(timer) * 60)))
            continue


        if mode == "stop":
            await kill()
            logger.logInfo("All timers have been killed.")
            continue

        if mode == "exit":
            sys.exit(0)
        
        # if no if block hit
        print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer','stop'. Got '{input_arr[0]}'.")


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
        logger.logInfo("Starting the application.")
        asyncio.run(main())
    except Exception as e:
        logger.logCritical(f"Critical error: {e=}" )
    finally:
        logger.logFatal("Terminating...")
        logger.logEmpty()
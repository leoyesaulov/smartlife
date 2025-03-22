import sys
import logger
import asyncio
import traceback
from asyncio import sleep
from light_switch import LightStrip
from data_handler import DataHandler


async def __run():
    while True:
        await __event.wait()
        __cololight_strip.check()
        logger.logInfo(f"Automated check has been performed.")
        await sleep(600)
        
def __parse(arr):
    out = {
        "command": arr[0],
        "param1": '25' if arr[0] == 'on' and arr[1] == 0 else arr[1],
        "param2": arr[2]
    }
    return out

async def __listen_to_input():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "")
        input_arr = user_input.lower().split()

        # padding the list
        input_arr = input_arr + [0]*(3-len(input_arr))
        
        input_dict = __parse(input_arr)

        # Command specification
        command = input_dict['command']
        # First parameter: brightness for on/off commands, duration for timer, desired city for city
        param1 = input_dict['param1']
        # Second parameter: timer for on/off commands
        param2 = input_dict['param2']
      
        if command == "on":
            __cololight_strip.on(int(param1))
            
            if param2:
                logger.logInfo(f"Timer of {param2} minutes has been set.")
                __extra_tasks.append(asyncio.create_task(__wait(int(param2) * 60)))
            
            continue

        if command == "off":
            __cololight_strip.off()
            
            if param2:
                logger.logInfo(f"Timer of {param2} minutes has been set.")
                __extra_tasks.append(asyncio.create_task(__wait(int(param2) * 60)))
            continue

        if command == "timer":
            logger.logInfo(f"Timer of {param2} minutes has been set.")
            __extra_tasks.append(asyncio.create_task(__wait(int(param2) * 60)))
            continue


        if command == "stop":
            await __kill()
            logger.logInfo("All timers have been killed.")
            continue

        if command == "city":
            if not param1:
                print(f"Current city is: '{__data_handler.get('''CITY''').capitalize()}'")
            else:
                __cololight_strip.change_location_with_param(param1)
                
            continue

        if command == "changeloc":
            __cololight_strip.change_location()
            continue

        if command == "exit":
            sys.exit(0)
        
        # if no if block hit
        print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer', 'stop', 'city', 'exit'. Got '{input_arr[0]}'.")


async def __wait(seconds):
    await __enter()
    await asyncio.sleep(seconds)
    logger.logInfo(f"Wait complete." )
    await __release()

async def __enter():
    global __semaphore
    async with __lock:
        __semaphore += 1
    __event.clear()

async def __release():
    global __semaphore
    async with __lock:
        __semaphore -= 1
        if __semaphore <= 0:
            __event.set()

async def __kill():
    global __extra_tasks
    global __semaphore
    async with __lock:
        for task in __extra_tasks:
            task.cancel()
        __semaphore = 0
        __event.set()

async def __main():
    __event.set()
    await asyncio.gather(__run(), __listen_to_input())

if __name__ == "__main__":
    try:
        logger.logInfo("Starting the application.")
        __event = asyncio.Event()
        __semaphore = 0
        __lock = asyncio.Lock()
        __extra_tasks = []
        __data_handler = DataHandler()
        __cololight_strip = LightStrip(ip=__data_handler.get("STRIP_IP"))

        asyncio.run(__main())
    except Exception as e:
        logger.logCritical(f"Critical error: {e=}\nStacktrace:\n{traceback.format_exc()}")
    finally:
        logger.logFatal("Terminating...")
        logger.logEmpty()
import asyncio
import sys
from dotenv import load_dotenv, find_dotenv, get_key
import logger
from asyncio import sleep
import light_switch


async def _run():
    while True:
        await event.wait()
        cololight_strip.check()
        logger.logInfo(f"Automated check has been performed.")
        await sleep(600)
        
def _parse(arr):
    out = {
        "command": arr[0],
        "param1": '25' if arr[0] == 'on' and arr[1] == 0 else arr[1],
        "param2": arr[2]
    }
    return out

def _get_from_env(key: str) -> str:
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    return get_key(dotenv_file, key)

async def listen_to_input():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "")
        input_arr = user_input.lower().split()

        # padding the list
        input_arr = input_arr + [0]*(3-len(input_arr))
        
        input_dict = _parse(input_arr)

        # Command specification
        command = input_dict['command']
        # First parameter: brightness for on/off commands, duration for timer, desired city for city
        param1 = input_dict['param1']
        # Second parameter: timer for on/off commands
        param2 = input_dict['param2']
      
        if command == "on":
            cololight_strip.on(int(param1))
            
            if param2:
                logger.logInfo(f"Timer of {param2} minutes has been set.")
                extra_tasks.append(asyncio.create_task(wait(int(param2) * 60)))
            
            continue

        if command == "off":
            cololight_strip.off()
            
            if param2:
                logger.logInfo(f"Timer of {param2} minutes has been set.")
                extra_tasks.append(asyncio.create_task(wait(int(param2) * 60)))
            continue

        if command == "timer":
            logger.logInfo(f"Timer of {param2} minutes has been set.")
            extra_tasks.append(asyncio.create_task(wait(int(param2) * 60)))
            continue


        if command == "stop":
            await _kill()
            logger.logInfo("All timers have been killed.")
            continue

        if command == "city":
            if not param1:
                print(f"Current city is: '{_get_from_env('''CITY''').capitalize()}'")
            else:
                cololight_strip.change_location_with_param(param1)
                
            continue

        if command == "changeloc":
            cololight_strip.change_location()
            continue

        if command == "exit":
            sys.exit(0)
        
        # if no if block hit
        print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer', 'stop', 'city', 'exit'. Got '{input_arr[0]}'.")


async def wait(seconds):
    await _enter()
    await asyncio.sleep(seconds)
    logger.logInfo(f"Wait complete." )
    await _release()

async def _enter():
    global semaphore
    async with lock:
        semaphore += 1
    event.clear()

async def _release():
    global semaphore
    async with lock:
        semaphore -= 1
        if semaphore <= 0:
            event.set()

async def _kill():
    global extra_tasks
    global semaphore
    async with lock:
        for task in extra_tasks:
            task.cancel()
        semaphore = 0
        event.set()

async def _main():
    event.set()
    await asyncio.gather(_run(), listen_to_input())

if __name__ == "__main__":
    try:
        logger.logInfo("Starting the application.")
        event = asyncio.Event()
        semaphore = 0
        lock = asyncio.Lock()
        extra_tasks = []
        load_dotenv()
        cololight_strip = light_switch.LightStrip(ip=_get_from_env("STRIP_IP"))

        asyncio.run(_main())
    except Exception as e:
        logger.logCritical(f"Critical error: {e=}\nStacktrace:\n{traceback.format_exc()}")
    finally:
        logger.logFatal("Terminating...")
        logger.logEmpty()
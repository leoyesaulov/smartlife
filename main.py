import sys
import asyncio
import traceback
from api import runApi
from logger import log
from asyncio import sleep
from common import  state
from devices import cololight_strip
from data_handler import DataHandler

import argparse


async def run():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    while True:
        await event.wait()
        if state.active:
            cololight_strip.check()
            log(f"Automated check has been performed.", "info")
        else:
            log(f"Inactive. Sleeping through the check", "info")
        await sleep(600)


async def listen_to_input():
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    
    # parser.add_argument()...

    while True:
        user_input = await loop.run_in_executor(None, input, "\r>>> ")
        log(f"User input: {user_input}", "info")

        parser.parse_args(user_input.split())

        # padding the list
        input_arr = input_arr + [0] * (3 - len(input_arr))

        input_dict = {
            "command": input_arr[0],
            "param1": input_arr[1],
            "param2": input_arr[2]
        }
        
        match input_dict:
            case {"command":"on", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.on(p1)
                if p2 != 0:
                    timer(p2)

            case {"command":"off", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.off()
                if p2 != 0:
                    timer(int(p2))
            
            case {"command":"timer", "param1":p1, "param2":p2}:
                p1: int
                p2: int
                timer(int(p1))

            case {"command":"stop", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                await kill()
                log("All timers have been killed.", "info", __print)
 
            case {"command":"city", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                if not p1:
                    print(f"Current city is: \'{data_handler.get('CITY').capitalize()}\'")
                else:
                    cololight_strip.change_location_with_param(p1)

            case {"command":"changeloc", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.change_location()

            case {"command":"state", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.get_state()

            case {"command":"refresh", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.check()

            case {"command":"help", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                __print("Available commands are: 'on', 'off', 'timer', 'stop', 'city', 'changeloc', 'state', 'refresh', 'help', 'exit'.")
               
            case {"command":"exit", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                sys.exit(0)

            case _:
                __print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer', 'stop', 'city', 'changeloc', 'state', 'refresh', 'exit'. Got '{input_arr[0]}'.")


        
def timer(duration: int):
    """
    Sets the timer of <duration> minutes.\n
    While the timer is active, no automated checks will be performed.
    :param duration:
    :return:
    """
    if duration >= 0:
        log(f"Timer of {duration} minutes has been set.", "info", __print)
        extra_tasks.append(asyncio.create_task(wait(int(duration) * 60)))
    else:
        log(f"Duration of {duration} minutes is invalid for timer function", "error", __print)


async def wait(seconds):
    await enter()
    await asyncio.sleep(seconds)
    log(f"Wait complete.",  "info", __print)
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
    await asyncio.gather(run(), listen_to_input(), runApi())


def exception_handler(loop, context):
    exception = context.get("exception")
    message = context.get("message")
    if type(exception) is not SystemExit:
        log(f"async exception has been raised: {exception} with message: {message}", "error")


def get_from_db(id):
    pass


def put_to_db(id, value):
    pass


def init_db():
    pass


def __print(msg: str) -> None:
    print(f"\r{msg}", flush=True)
    print(">>> ", end="", flush=True)

if __name__ == "__main__":
    device_counter = 0
    devices = {}
    event = asyncio.Event()
    semaphore = 0
    lock = asyncio.Lock()
    extra_tasks = []
    data_handler = DataHandler()

    try:
        log("Starting the application.", "info", __print)
        asyncio.run(main())
    except SystemExit as e:
        print("\rExiting peacefully...", flush=True)
    except KeyboardInterrupt:
        log("Keyboard interrupt.", "info")
        print("\rExiting peacefully...", flush=True)
    except Exception as error:
        log(f"Critical error: {error=}\nStacktrace:\n{traceback.format_exc()}", "critical")
        print(f"\rCritical error: {error=}", flush=True)
    finally:
        log("Terminating...\n", "critical")

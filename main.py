import sys
import asyncio
import traceback

from api import runApi, active
from logger import log
from asyncio import sleep
from devices import cololight_strip
from data_handler import DataHandler

import argparse


async def run():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    while True:
        await event.wait()
        if active:
            cololight_strip.check()
            log(f"Automated check has been performed.", "info")
        else:
            log(f"Inactive. Sleeping through the check", "info")
        await sleep(600)


def parse(arr):
    out = {
        "command": arr[0],
        "param1": '25' if arr[0] == 'on' and arr[1] == 0 else arr[1],
        "param2": arr[2]
    }
    return out


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

        input_dict = parse(input_arr)

        # Command specification
        command = input_dict['command']
        # First parameter: brightness for on/off commands, duration for timer, desired city for city
        param1 = input_dict['param1']
        # Second parameter: timer for on/off commands
        param2 = input_dict['param2']

        if command == "on":
            cololight_strip.on(int(param1))

            if param2:
                timer(int(param2))

            continue

        if command == "off":
            cololight_strip.off()

            if param2:
                timer(int(param2))
            continue

        if command == "timer":
            timer(int(param1))
            continue

        if command == "stop":
            await kill()
            log("All timers have been killed.", "info", __print)
            continue

        if command == "city":
            if not param1:
                print(f"Current city is: '{data_handler.get('''CITY''').capitalize()}'")
            else:
                cololight_strip.change_location_with_param(param1)

            continue

        if command == "changeloc":
            cololight_strip.change_location()
            continue

        if command == "state":
            cololight_strip.get_state()
            continue

        if command == "refresh":
            cololight_strip.check()
            continue

        if command == "help":
            __print("Available commands are: 'on', 'off', 'timer', 'stop', 'city', 'changeloc', 'state', 'refresh', 'help', 'exit'.")
            continue

        if command == "exit":
            sys.exit(0)

        # if no if block hit
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

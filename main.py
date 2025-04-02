import sys
import asyncio
import traceback
from logger import log
from asyncio import sleep
from colo_strip import ColoStrip
from data_handler import DataHandler


async def __run():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(__exception_handler)
    while True:
        await __event.wait()
        __cololight_strip.check()
        log(f"Automated check has been performed.", "info")
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
        user_input = await loop.run_in_executor(None, input, "\r>>> ")
        log(f"User input: {user_input}", "info")
        input_arr = user_input.lower().split()

        # padding the list
        input_arr = input_arr + [0] * (3 - len(input_arr))

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
                __timer(int(param2))

            continue

        if command == "off":
            __cololight_strip.off()

            if param2:
                __timer(int(param2))
            continue

        if command == "timer":
            __timer(int(param1))
            continue

        if command == "stop":
            await __kill()
            log("All timers have been killed.", "info")
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

        if command == "state":
            __cololight_strip.get_state()
            continue

        if command == "refresh":
            __cololight_strip.check()
            continue

        if command == "exit":
            sys.exit(0)

        # if no if block hit
        print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer', 'stop', 'city', 'exit'. Got '{input_arr[0]}'.")

def __timer(duration: int):
    """
    Sets the timer of <duration> minutes.\n
    While the timer is active, no automated checks will be performed.
    :param duration:
    :return:
    """
    if duration >= 0:
        log(f"Timer of {duration} minutes has been set.", "info", __print)
        __extra_tasks.append(asyncio.create_task(__wait(int(duration) * 60)))
    else:
        log(f"Duration of {duration} minutes is invalid for timer function", "error", __print)


async def __wait(seconds):
    await __enter()
    await asyncio.sleep(seconds)
    log(f"Wait complete.",  "info", __print)
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


def __exception_handler(loop, context):
    exception = context.get("exception")
    message = context.get("message")
    if type(exception) is not SystemExit:
        log(f"async exception has been raised: {exception} with message: {message}", "error")


def __get_from_db(id):
    pass


def __put_to_db(id, value):
    pass


def __init_db():
    pass


def __print(msg: str) -> None:
    print(f"\r{msg}", flush=True)
    print(">>> ", end="", flush=True)

if __name__ == "__main__":
    __device_counter = 0
    __devices = {}
    __event = asyncio.Event()
    __semaphore = 0
    __lock = asyncio.Lock()
    __extra_tasks = []
    __data_handler = DataHandler()

    try:
        log("Starting the application.", "info", print)
        __cololight_strip = ColoStrip(ip=__data_handler.get("STRIP_IP"), id=__device_counter)
        __device_counter += 1

        asyncio.run(__main())
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

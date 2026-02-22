import sys
import traceback

import time
import threading

import common
from api import runApi
from logger import log
from common import  state
from devices import cololight_strip
from data_handler import DataHandler


# ToDo: ensure correct concurrency, clean up and test

def run_checks():
    while True:
        wait_for_timers()
        if state.service_active:
            cololight_strip.check()
            log(f"Automated check has been performed.", "info", __print)
        else:
            log(f"Inactive. Sleeping through the check", "info", __print)
        time.sleep(5)

def wait_for_timers():
    while len(sleeping_queue) > 0:
        thread = sleeping_queue[0]
        thread.join()
        sleeping_queue.remove(thread)

# Todo: the script seems to ignore cli inputs???
def listen_to_input():
    while True:
        user_input = input("\r>>> ")
        log(f"User input: {user_input}", "info")

        input_arr = user_input.lower().split()

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

                # default brightness should be 25
                cololight_strip.on(25 if p1 == 0 else p1)
                if p2 != 0:
                    timer(p2)

            case {"command":"off", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                cololight_strip.off()
                if p2 != 0:
                    timer(p2)
            
            case {"command":"timer", "param1":p1, "param2":p2}:
                p1: int
                p2: int
                timer(int(p1))

            case {"command":"stop", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                kill()
                log("All timers have been killed.", "info", __print)
 
            case {"command":"city", "param1":p1, "param2":p2}:
                p1: int
                p2: int

                if p1 != 0:
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

            case {"command":"status", "param1":p1, "param2":p2}:
                print(f"Current service status: owner_present: {common.state.owner_present}, service_active: {common.state.service_active}")

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
        sleeping_thread = threading.Thread(target=wait(int(duration) * 60))
        sleeping_queue.append(sleeping_thread)
        sleeping_thread.start()
    else:
        log(f"Duration of {duration} minutes is invalid for timer function", "error", __print)


def wait(seconds):
    time.sleep(seconds)
    log(f"Wait complete.",  "info", __print)


# sidenote: wtf was I thinking goddamnit
# async def enter():
#     global semaphore
#     async with lock:
#         semaphore += 1
#     event.clear()
#
#
# async def release():
#     global semaphore
#     async with lock:
#         semaphore -= 1
#         if semaphore <= 0:
#             event.set()


def kill():
    global sleeping_queue
    global semaphore
    sleeping_queue.clear()

    # semaphore = 0
    # event.set()


def exception_handler(loop, context):
    exception = context.get("exception")
    message = context.get("message")
    if type(exception) is not SystemExit:
        log(f"async exception has been raised: {exception} with message: {message}", "error", __print)


def __print(msg: str) -> None:
    print(f"\r{msg}", flush=True)
    print(">>> ", end="", flush=True)

# ToDO add proper logging
if __name__ == "__main__":
    device_counter = 0
    devices = {}
    semaphore = threading.Semaphore()
    sleeping_queue = []
    data_handler = DataHandler()

    try:
        log("Starting the application.", "info", __print)
        checking_thread = threading.Thread(target=run_checks())
        checking_thread.start()

        log("Checking thread started.", "info", __print)

        cli_thread = threading.Thread(target=listen_to_input())
        cli_thread.start()

        log("CLI thread started.", "info", __print)

        api_thread = threading.Thread(target=runApi())
        api_thread.start()

        log("API thread started.", "info", __print)

        checking_thread.join()
        cli_thread.join()
        api_thread.join()
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

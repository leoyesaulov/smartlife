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

        # padding the list
        input_arr = input_arr + [0]*(3-len(input_arr))

        if input_arr[0] == "on":
            light_switch.on(int(input_arr[1]))
            
            if input_arr[2]:
                print(f"waiting {input_arr[2]} minutes, starting at {datetime.now().strftime('%H:%M:%S')}")
            
            extra_tasks.append(asyncio.create_task(wait(int(input_arr[2]) * 60)))
            continue

        if input_arr[0] == "off":
            light_switch.off()
            extra_tasks.append(asyncio.create_task(wait(int(input_arr[1]) * 60)))
            continue

        if input_arr[0] == "timer":
            extra_tasks.append(asyncio.create_task(wait(int(input_arr[1]) * 60)))
            continue


        if input_arr[0] == "stop":
            await kill()
            continue
        
        # if no if block hit
        print(f"I'm sorry, I didn't understand that.\nExpected one of: 'on', 'off', 'timer','stop'. Got '{input_arr[0]}'.")
                


async def wait(seconds):
    await enter()
    await asyncio.sleep(seconds)
    print(f"wait complete at {datetime.now().strftime("%H:%M:%S")}")
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
    asyncio.run(main())
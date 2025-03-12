import os
import datetime
from astral.sun import sun
from astral import LocationInfo
from dotenv import load_dotenv
from pycololight import PyCololight


load_dotenv()
strip = PyCololight(device="strip", host=os.getenv("STRIP_IP"), dynamic_effects=True)
city = LocationInfo("Munich", "Germany", "Europe/Berlin", 48.13743, 11.57549) # You think it's a good idea to write the exact city you live in to a public repository?
utc = datetime.timezone(datetime.timedelta(hours=0)) # unused variable
munich = datetime.timezone(datetime.timedelta(hours=+1)) # Change to "tz" for porability purposes?


def check():
    sunset = sun(city.observer)["sunset"].astimezone(munich)
    now = datetime.datetime.now().astimezone(munich)
    strip.state # the statement has no effect?

    if now >= sunset - datetime.timedelta(minutes=30) and not all([strip.on, now.hour == 23]):
        print(f"Turning lights on with previous brightness ({strip.brightness}) at {now.astimezone().strftime("%d.%b.%Y %H:%M:%S")}")
        on()
    if (now.hour >= 23 or (0 <= now.hour <= 8)) and int(now.minute/10) % 3 == 0 and strip.on:
        print(f"Turning lights off at {now.strftime("%d.%b.%Y %H:%M:%S")}")
        off()

def on(brightness=25):
    strip.on = brightness

def off():
    strip.on = 0
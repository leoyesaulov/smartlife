import os
import datetime
from astral.sun import sun
from astral import LocationInfo
from dotenv import load_dotenv
from pycololight import PyCololight


load_dotenv()
strip = PyCololight(device="strip", host=os.getenv("STRIP_IP"), dynamic_effects=True)
city = LocationInfo("Munich", "Germany", "Europe/Berlin", 48.13743, 11.57549)
utc = datetime.timezone(datetime.timedelta(hours=0))
munich = datetime.timezone(datetime.timedelta(hours=+1))


def check():
    sunset = sun(city.observer)["sunset"].astimezone(munich)
    now = datetime.datetime.now().astimezone(munich)
    strip.state

    if now >= sunset - datetime.timedelta(minutes=30) and not strip.on:
        print("Turning lights on with previous brightness: ", strip.brightness, " at: " + now.astimezone().strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 25
    if now.day != (now + datetime.timedelta(minutes=30)).day and strip.on:
        print("Turning lights off at: " + now.strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 0

def on(brightness=25):
    strip.on = brightness

def off():
    strip.on = 0
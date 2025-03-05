import os
import datetime
from astral.sun import sun
from astral import LocationInfo
from dotenv import load_dotenv
from pycololight import PyCololight


load_dotenv()
strip = PyCololight(device="strip", host=os.getenv("STRIP_IP"), dynamic_effects=True)
city = LocationInfo("Munich", "Germany", "Europe/Berlin", 48.13743, 11.57549)
strip.on = 0
utc = datetime.timezone(datetime.timedelta(hours=0))
munich = datetime.timezone(datetime.timedelta(hours=+1))


def check():
    sunset = sun(city.observer)["sunset"].astimezone(munich)
    sunrise = sun(city.observer)["sunrise"].astimezone(munich)
    now = datetime.datetime.now().astimezone(munich)

    if now >= sunset - datetime.timedelta(minutes=30) and (strip.brightness == 0 or strip.brightness is None):
        print("Turning lights on with previous brightness: ", strip.brightness, " at: " + now.astimezone().strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 25
    if now <= sunrise + datetime.timedelta(minutes=30) and strip.brightness > 0:
        print("Turning lights off at: " + now.strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 0
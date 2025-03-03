import os
import datetime
from astral.sun import sun
from astral import LocationInfo
from dotenv import load_dotenv
from pycololight import PyCololight


load_dotenv()
strip = PyCololight(device="strip", host=os.getenv("STRIP_IP"), dynamic_effects=True)
city = LocationInfo("Munich", "Germany", "Europe/Berlin", 48.13743, 11.57549)

sunset = sun(city.observer)["sunset"]
sunrise = sun(city.observer)["sunrise"]
now = datetime.datetime.now().astimezone()

def check():
    if now >= sunset - datetime.timedelta(minutes=30):
        print("Turning lights on at: " + now.strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 25
    if now <= sunrise + datetime.timedelta(minutes=30):
        print("Turning lights off at: " + now.strftime("%d.%b.%Y %H:%M:%S"))
        strip.on = 0
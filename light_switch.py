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
now = datetime.datetime.now().astimezone()

def check():
    if now >= sunset - datetime.timedelta(minutes=30):
        strip.on = 25
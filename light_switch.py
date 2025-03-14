import os
import datetime
import logger
from astral.sun import sun
from astral import LocationInfo
from dotenv import load_dotenv
from pycololight import PyCololight


class LightStrip:
    def __init__(self, ip, device='cololight'):
        load_dotenv()
        self.city = LocationInfo(os.getenv("CITY"), os.getenv("COUNTRY"), os.getenv("TIMEZONE"), float(os.getenv("LATITUDE")), float(os.getenv("LONGITUDE")))
        self.city_tz = datetime.timezone(datetime.timedelta(hours=+1))
        match device:
            case "cololight":
                self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)

    def check(self):
        sunset = sun(self.city.observer)["sunset"].astimezone(self.city_tz)
        now = datetime.datetime.now().astimezone(self.city_tz)
        self.strip.state

        if now >= sunset - datetime.timedelta(minutes=30) and not any([self.strip.on, now.hour == 23]):
            self.on()
        if (now.hour >= 23 or (0 <= now.hour <= 8)) and int(now.minute/10) % 3 == 0 and self.strip.on:
            self.off()

    def on(self, brightness=25):
        self.strip.state
        logger.logInfo(f"Turning lights on with previous brightness: {self.strip.brightness}.")
        self.strip.on = brightness

    def off(self):
        logger.logInfo(f"Turning lights off.")
        self.strip.on = 0
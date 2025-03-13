import datetime
import logger
from astral.sun import sun
from astral import LocationInfo, Observer
from dotenv import load_dotenv
from pycololight import PyCololight
from geopy.geocoders import Nominatim
from typing import Dict, Union


def get_user_location(agent: str = "smartlife") -> Dict[str, Union[Observer, datetime.timezone]]:
    """
    Prompts the user to enter their location until a valid input is given.
    Returns a dictionary with:
        observer: astral.Observer\n
        timezone: datetime.timezone
    """
    loc = {}
    while True:
        usr_input = input("Please provide an (approximate) location of the strip: ")
        if not usr_input: continue

        try:
            # convert location to (among others) latitude and longitude
            user_code = Nominatim(user_agent=agent).geocode(usr_input)
            observer = LocationInfo(latitude=user_code.latitude, longitude=user_code.longitude).observer

            loc.update({"observer": observer})
            loc.update({"timezone": datetime.timezone(observer.utcoffset(dt=None))})

            # not sure about Nominatim's behaviour
            assert all(loc.values()), "Error has occurred while filling the location dictionary: the dict is empty"
            return loc
        except Exception as err:
            print(f"An error occurred while parsing user's input: {err}")


class LightStrip:
    def __init__(self, ip, device='cololight'):
        load_dotenv()
        user_loc = get_user_location()
        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]
        match device:
            case "cololight":
                self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)

    def check(self):
        sunset = sun(self.city)["sunset"].astimezone(self.city_tz)
        now = datetime.datetime.now().astimezone(self.city_tz)
        self.strip.state

        if now >= sunset - datetime.timedelta(minutes=30) and not all([self.strip.on, now.hour == 23]):
            self.on()
        if (now.hour >= 23 or (0 <= now.hour <= 8)) and int(now.minute / 10) % 3 == 0 and self.strip.on:
            self.off()

    def on(self, brightness=25):
        self.strip.state
        logger.logInfo(f"Turning lights on with previous brightness: {self.strip.brightness}.")
        self.strip.on = brightness

    def off(self):
        logger.logInfo(f"Turning lights off.")
        self.strip.on = 0

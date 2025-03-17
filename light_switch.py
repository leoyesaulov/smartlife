import os
import logger
from astral.sun import sun
from pycololight import PyCololight
from dotenv import find_dotenv, load_dotenv, set_key

# related to ID'ing the location
from typing import Dict, Union
from geopy.geocoders import GeoNames
from astral import LocationInfo, Observer
from datetime import datetime, timezone, timedelta


def _update_env(key: str, value: str):
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    set_key(dotenv_file, key, value)

def _get_dict(string: str, username: str = "smartlife"):
    return GeoNames(username).geocode(string)

def _ask_for_input(username: str = "smartlife"):
    """
    Helper function that pulls environment and/or prompts the user for input
    :param username:
    :return: res of .geocode()
    """
    while True:
        city = os.environ.get("CITY")
        if not city:
            user_input = input("Please provide the city your strip is located in: ")
            if not user_input:
                continue

            res = GeoNames(username).geocode(user_input)
            if res:
                _update_env("CITY", user_input)
                break

            print(f"City '{user_input}' could not be found, try a different one.")

        else:
            res = GeoNames(username).geocode(city)
            if not res:
                _update_env("CITY", "")
                print(f"City '{city}' was pulled from environment and could not be found, try a different one.")
                continue
            else:
                logger.logInfo(f"Pulled the city '{city}' from environment successfully.")
                break

    return res

def _res_to_loc(res, username: str = "smartlife"):
    loc: Dict[str, Union[Observer, timezone]] = {"observer": None, "timezone": None}

    coordinates = res.point
    gmt_offset = GeoNames(username).reverse_timezone(coordinates).raw["gmtOffset"]
    tz = timezone(timedelta(hours=gmt_offset))
    loc.update({"timezone": tz})

    # needed further down the line
    observer = LocationInfo(latitude=coordinates.latitude, longitude=coordinates.longitude).observer
    loc.update({"observer": observer})

    assert all(loc.values()), "Error has occurred while filling the location dictionary: the dict is empty"
    return loc


def _get_user_location(username: str = "smartlife") -> Dict[str, Union[Observer, timezone]]:
    """
    Loads from environment or prompts the user to enter their location until a valid input is given.
    Returns a dictionary with:
        observer: astral.Observer\n
        timezone: datetime.timezone
    """

    res = _ask_for_input(username)
    return _res_to_loc(res, username)


class LightStrip:
    def __init__(self, ip, device='cololight'):
        load_dotenv()
        user_loc = _get_user_location()
        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]
        match device:
            case "cololight":
                self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)

    def change_location(self, city: str):
        res = _ask_for_input(city)
        if not res:
            print(f"I was unable to find city '{city}'. Try again.")
            return
        _update_env("CITY", city)
        loc = _res_to_loc(res)                                                      # ToDo: usernames not supported here, fix when multi-devicing
        self.city = loc["observer"]
        self.city_tz = loc["timezone"]

    def check(self):
        sunset = sun(self.city)["sunset"].astimezone(self.city_tz)
        now = datetime.now().astimezone(self.city_tz)
        self.strip.state

        if now >= sunset - timedelta(minutes=30) and not any([self.strip.on, now.hour == 23]):
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

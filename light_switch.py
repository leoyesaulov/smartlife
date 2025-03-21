import os
import logger
from astral.sun import sun
from pycololight import PyCololight
from dotenv import find_dotenv, load_dotenv, set_key

# related to ID'ing the location
from typing import Dict, Union, Tuple, Any
from geopy.geocoders import GeoNames
from astral import LocationInfo, Observer
from datetime import datetime, timezone, timedelta


def _log_to_env(value: str, key: str = "CITY") -> None:
    """
    Logs value as key in the .env
    """
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    set_key(dotenv_file, key, value)
    return

def _str_to_res(city: str, username: str = "smartlife") -> Any:
    return GeoNames(username).geocode(city)

def _res_to_loc(res: Any, username: str = "smartlife") -> Dict[str, Union[Observer, timezone]]:
    loc: Dict[str, Union[Observer, timezone]] = {"observer": None, "timezone": None}

    coordinates = res.point
    gmt_offset = GeoNames(username).reverse_timezone(coordinates).raw["gmtOffset"]
    tz = timezone(timedelta(hours=gmt_offset))
    loc.update({"timezone": tz})

    observer = LocationInfo(latitude=coordinates.latitude, longitude=coordinates.longitude).observer
    loc.update({"observer": observer})

    assert all(loc.values()), "Error has occurred while filling the location dictionary: the dict is empty"

    return loc


def _get_user_location(preset_loc: str = None, username: str = "smartlife") -> Tuple[
    Dict[str, Union[Observer, timezone]], str]:
    """
    Parses user's location into Observer object and timezone.\n
    Unless preset_loc is given, prompts the user to enter their location until a valid input is given.\n
    Dictionary with:
        observer: astral.Observer\n
        timezone: datetime.timezone
    :returns: Dictionary
    """
    while True:
        # preset_loc MUST be valid, unless we want the app to get stuck in the loop
        if preset_loc:
            usr_input = preset_loc
        else:
            usr_input = input("Please provide the city your strip is located in: ")

        if not usr_input: continue

        res = _str_to_res(usr_input, username)
        if res: break

        print(f"City '{usr_input}' could not be found, try a different one.")

    return _res_to_loc(res), usr_input


class LightStrip:
    def __init__(self, ip, device='cololight'):
        preset_loc = os.environ.get("CITY")
        # A reminder to the user
        if preset_loc:
            print(f"Your location is: {preset_loc.capitalize()}.\n"
                  f"To change it run 'city <param>' or 'changeloc'.")
        user_loc, user_inp = _get_user_location(preset_loc=preset_loc)

        _log_to_env(key="CITY", value=user_inp)

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        if device == "cololight":
            self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)
        # adding other devices as time goes on
        else:
            raise ValueError(f"Your device {device} is not supported.")
        return

    def change_location(self):
        user_loc, user_inp = _get_user_location()

        _log_to_env(key="CITY", value=user_inp)

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        print(f"Current city has been updated to '{user_inp.capitalize()}'.")
        logger.logInfo(f"Current city has been updated to '{user_inp.capitalize()}'.")
        return

    def change_location_with_param(self, city: str):
        res = _str_to_res(city)
        if not res:
            print(f"City '{city}' could not be found, try a different one.")
            return

        loc = _res_to_loc(res)

        _log_to_env(key="CITY", value=city)

        self.city = loc["observer"]
        self.city_tz = loc["timezone"]
        print(f"Current city has been updated to '{city.capitalize()}'.")
        logger.logInfo(f"Current city has been updated to '{city.capitalize()}'.")
        return

    def check(self):
        self.strip.state
        sunset = sun(self.city)["sunset"].astimezone(self.city_tz)
        now = datetime.now().astimezone(self.city_tz)

        if now >= sunset - timedelta(minutes=30) and not any([self.strip.on, now.hour == 23]):
            self.on()
        if (now.hour >= 23 or (0 <= now.hour <= 8)) and int(now.minute / 10) % 3 == 0 and self.strip.on:
            self.off()

    def on(self, brightness=25):
        self.strip.state
        logger.logInfo(f"Turning lights on with previous brightness: {self.strip.brightness}.")
        self.strip.on = brightness

    def off(self):
        self.strip.state
        logger.logInfo("Turning the lights off.")
        self.strip.on = 0

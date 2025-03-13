import logger
from astral.sun import sun
from dotenv import load_dotenv
from pycololight import PyCololight

# related to ID'ing the location
from typing import Dict, Union
from geopy.geocoders import GeoNames
from astral import LocationInfo, Observer
from datetime import datetime, timezone, timedelta


def get_user_location(username: str = "smartlife") -> Dict[str, Union[Observer, timezone]]:
    """
    Prompts the user to enter their location until a valid input is given.
    Returns a dictionary with:
        observer: astral.Observer\n
        timezone: datetime.timezone
    """
    loc: Dict[str, Union[Observer, timezone]] = {"observer": None, "timezone": None}

    while True:
        usr_input = input("Please provide the city your strip is located in: ")
        if not usr_input: continue

        res = GeoNames(username).geocode(usr_input)
        if res: break

        print(f"City '{usr_input}' could not be found, try a different one.")

    coordinates = res.point
    gmt_offset = GeoNames(username).reverse_timezone(coordinates).raw["gmtOffset"]
    tz = timezone(timedelta(hours=gmt_offset))
    loc.update({"timezone": tz})

    # needed further down the line
    observer = LocationInfo(latitude=coordinates.latitude, longitude=coordinates.longitude).observer
    loc.update({"observer": observer})

    assert all(loc.values()), "Error has occurred while filling the location dictionary: the dict is empty"
    return loc


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
        now = datetime.now().astimezone(self.city_tz)
        self.strip.state

        if now >= sunset - timedelta(minutes=30) and not all([self.strip.on, now.hour == 23]):
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

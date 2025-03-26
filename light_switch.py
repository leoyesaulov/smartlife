import logger
from astral.sun import sun
from pycololight import PyCololight
from city_handler import CityHandler
from data_handler import DataHandler

# related to ID'ing the location
from datetime import datetime, timedelta

class LightStrip:
    def __init__(self, ip, device='cololight'):
        self.__data_handler = DataHandler()
        preset_loc = self.__data_handler.get("CITY")
        self.__city_handler = CityHandler()
        # A reminder to the user
        if preset_loc:
            print(f"Your location is: {preset_loc.capitalize()}.\n"
                  f"To change it run 'city <param>' or 'changeloc'.")

        user_loc, _ = self.__city_handler.city_flow(preset_loc=preset_loc)

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        if device == "cololight":
            self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)
        # adding other devices as time goes on
        else:
            raise ValueError(f"Your device {device} is not supported.")
        return

    def change_location(self):
        user_loc, user_inp = self.__city_handler.city_flow()

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        logger.logInfo(f"Current city has been updated to '{user_inp.capitalize()}'.", print)
        return

    def change_location_with_param(self, city: str):
        loc = self.__city_handler.city_change(city)
        if not loc: return

        self.city = loc["observer"]
        self.city_tz = loc["timezone"]

        logger.logInfo(f"Current city has been updated to '{city.capitalize()}'.", print)
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
        logger.logInfo(f"Turning lights on with previous brightness: {self.strip.brightness}.", print)
        self.strip.on = brightness

    def off(self):
        self.strip.state
        logger.logInfo("Turning the lights off.", print)
        self.strip.on = 0
        self.strip.brightness = 0    # Temporary fix until the pycololight library is fixed


    def get_state(self):
        self.strip.state
        print(self.strip.brightness)
import traceback
from common import state
from logger import log
from time import sleep
from astral.sun import sun
from pycololighto import PyCololight
from city_handler import CityHandler
from data_handler import DataHandler

# related to ID'ing the location
from datetime import datetime, timedelta


def _print(msg: str) -> None:
    print(f"\r{msg}", flush=True)
    print(">>> ", end="", flush=True)

class ColoStrip:
    def check_connection(self):
        error = None
        for word in ["First", "Second"]:
            try:
                self.strip.state()
                return
            except Exception as err:
                print(f"{word} attempt to connect failed")
                log(f"{word} attempt failed: {err=}\nStacktrace:\n{traceback.format_exc()}", "critical")
                error = err
                sleep(1)

        if error:
            log("Could not connect to Strip.", "error")
            raise error

        return

    def __init__(self, ip, id, device='cololight'):
        self.id = id
        self.data_handler = DataHandler()
        preset_loc = self.data_handler.get("CITY")
        self.city_handler = CityHandler()
        # A reminder to the user
        if preset_loc:
            print(f"Your location is: {preset_loc.capitalize()}.\n"
                  f"To change it run 'city <param>' or 'changeloc'.")

        user_loc, _ = self.city_handler.city_flow(preset_loc=preset_loc)

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        if device == "cololight":
            self.strip = PyCololight(device="strip", host=ip, dynamic_effects=True)
        # adding other devices as time goes on
        else:
            raise ValueError(f"Your device {device} is not supported.")

        self.check_connection()
        return

    def change_location(self):
        user_loc, user_inp = self.city_handler.city_flow()

        self.city = user_loc["observer"]
        self.city_tz = user_loc["timezone"]

        log(f"Current city has been updated to '{user_inp.capitalize()}'.", "info", print)
        return

    def change_location_with_param(self, city: str):
        loc = self.city_handler.city_change(city)
        if not loc: return

        self.city = loc["observer"]
        self.city_tz = loc["timezone"]

        log(f"Current city has been updated to '{city.capitalize()}'.", "info", print)
        return

    def check(self):
        self.strip.state()
        sunset = sun(self.city)["sunset"].astimezone(self.city_tz)
        now = datetime.now().astimezone(self.city_tz)

        # owner_present: true if owner connected to home network, false otherwise
        # if not home - turn off. If home and otherwise approved - turn on
        if (now >= sunset - timedelta(minutes=30) and not any([self.strip.on, now.hour == 23])) and state.owner_present:
            self.on()
        if ((now.hour >= 23 or (0 <= now.hour <= 8)) and int(now.minute / 10) % 3 == 0 and self.strip.on) or not state.owner_present:
            self.off()

    def on(self, brightness=25):
        self.strip.state()
        log(f"Turning lights on with previous brightness: {self.strip.brightness}.", "info", _print)
        self.strip.on = brightness

    def off(self):
        self.strip.state()
        log("Turning lights off.", "info", _print)
        self.strip.on = None

    def get_state(self):
        self.strip.state()
        print(self.strip.brightness)

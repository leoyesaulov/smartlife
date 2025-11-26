from data_handler import DataHandler
from geopy.geocoders import GeoNames
from datetime import timezone, timedelta
from astral import LocationInfo, Observer
from typing import Dict, Union, Tuple, Any

class CityHandler:
    def __init__(self, username: str = "smartlife"):
        self.username = username
        self.data_handler = DataHandler()

    def city_flow(self, preset_loc: str = None) -> Tuple[
        Dict[str, Union[Observer, timezone]], str]:
        user_loc, user_inp = self.get_user_location(preset_loc=preset_loc, username=self.username)
        self.data_handler.write("CITY", user_inp)
        return user_loc, user_inp

    def city_change(self, city: str) -> Dict[str, Union[Observer, timezone]] | None:
        res = self.str_to_res(city)
        if not res:
            print(f"City '{city}' could not be found, try a different one one more time.")
            return None

        loc = self.res_to_loc(res)

        self.data_handler.write(key="CITY", value=city)

        return loc

    def str_to_res(self, city: str, username: str = "smartlife") -> Any:
        return GeoNames(username).geocode(city)

    def res_to_loc(self, res: Any, username: str = "smartlife") -> Dict[str, Union[Observer, timezone]]:
        loc: Dict[str, Union[Observer, timezone]] = {"observer": None, "timezone": None}

        coordinates = res.point
        gmt_offset = GeoNames(username).reverse_timezone(coordinates).raw["gmtOffset"]
        tz = timezone(timedelta(hours=gmt_offset))
        loc.update({"timezone": tz})

        observer = LocationInfo(latitude=coordinates.latitude, longitude=coordinates.longitude).observer
        loc.update({"observer": observer})

        assert all(loc.values()), "Error has occurred while filling the location dictionary: the dict is empty"

        return loc

    def get_user_location(self, preset_loc: str = None, username: str = "smartlife") -> Tuple[
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

            res = self.str_to_res(usr_input, username=username)
            if res: break

            print(f"City '{usr_input}' could not be found, try a different one.")

        return self.res_to_loc(res), usr_input
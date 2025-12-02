"""
This file defines and explains CityHandler class, which is responsible for everything regarding handling of user's location.
"""

from data_handler import DataHandler

from geopy.geocoders import GeoNames
from geopy.location import Location
from astral import LocationInfo, Observer

from datetime import timezone, timedelta

from typing import Dict, Union, Tuple, Any
from warnings import warn



class CityHandler:
    """
    CityHandler class is reponsible for everything related to user location.\n
    Avaialable attributes are:\n
        - username: ...
        - data_handler: DataHandler object
    
    Available methods are:
    - 

    """
    def __init__(self, username: str = "smartlife") -> None:
        self.username = username
        self.data_handler = DataHandler()

    
    def change_city(
            self, 
            city: str
    ) -> Dict[str, Union[Observer, timezone]] | None:
        """
        Parses new city\n
        Writes it with DataHandler instance\n

        :Params:
            - city: user's city
        :returns:
            - Observer object
            - timezone object

        :raises:
            - ValueError: if the city is invalid
        """
        res = self.str_to_loc(city)
        if not res:
            raise ValueError(f"The city '{city}' is invalid")

        loc = self.split_location(res)
        self.data_handler.write(key="CITY", value=city)
        return loc


    def str_to_loc(
            self, 
            city: str, 
            username: str = "smartlife"
    ) -> Location:
        """
        Parse city name to Location object
        :returns:
            - Location object with user's location
        :raises:
            - ValueError: if location could not be inferred
        """
        geonames = GeoNames(username)
        res = geonames.geocode(city)
        
        if not res:
            raise ValueError("Unable to infer location")

        res: Location
        return res


    def split_location(
        self,
        loc: Location,
        username: str = "smartlife"
    ) -> Dict[str, Union[Observer, timezone]]:
        pass
        """
        Splits Location object into a dictionary with astral.Observer and datetime.timezone object
        :Params:
            - res: ...
            - username: unsused for now
        
        :returns:
            - Dictionary with "observer" and "timezone" key keys
        """
        res: Dict[str, Union[Observer, timezone]] = {"observer": None, "timezone": None}

        coordinates = loc.point
        gmt_offset = GeoNames(username).reverse_timezone(coordinates).raw["gmtOffset"]
        tz = timezone(timedelta(hours=gmt_offset))
        res.update({"timezone": tz})

        observer = LocationInfo(latitude=coordinates.latitude, longitude=coordinates.longitude).observer
        res.update({"observer": observer})

        assert all(res.values()), "Error has occurred while filling the location dictionary: the dict is empty"
        return res


    def get_user_location(
            self, 
            preset_loc: str | None = None, 
            username: str = "smartlife"
    ) -> Tuple[
        Dict[str, Union[Observer, timezone]], 
        str
    ]:
        """
        Unless preset_loc is given, prompts the user to enter their location until a valid input is given.\n
        Parses user's location into Observer object and timezone.\n
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

            res = self.split_location(usr_input, username=username)
            if res: break

            print(f"City '{usr_input}' could not be found, try a different one.")
        # TODO
        return self.res_to_loc(res), usr_input


    # Deprecated functions
    # >>>>>
    def city_flow(
            self, 
            preset_loc: str | None = None
    ) -> Tuple[
        Dict[str, Union[Observer, timezone]], 
        str
    ]:
        """
        Calls get_user_location method\n
        Writes user location to CITY key using own DataHandler instance\n\n
        
        :Params:
            - preset_loc: the preset user location

        :returns:
            - user_loc
            - user_inp: user input
        """
        warn(
            "This function is deprecated, "
            "use self.get_user_location + self.data_handler.write separately or self.change_city"
        )

        user_loc, user_inp = self.get_user_location(preset_loc=preset_loc, username=self.username)
        self.data_handler.write("CITY", user_inp)
        return user_loc, user_inp


    def city_change(
            self, 
            *args,
            **kwargs
    ) -> Dict[str, Union[Observer, timezone]] | None:
        """
        Wrapper for change_city. Deprecated
        """
        warn("This function is deprecated, use self.change_city instead", DeprecationWarning)
        return self.change_city(*args,**kwargs)


    def res_to_loc(
            self, 
            *args,
            **kwargs
    ) -> Dict[str, Union[Observer, timezone]]:
        """
        This function is deprecated, use self.split_location instead
        """
        warn("This function is deprecated, use self.split_location instead", DeprecationWarning)
        return self.split_location(*args,**kwargs)
    # <<<<<


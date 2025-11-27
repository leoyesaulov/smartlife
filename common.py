from colo_strip import ColoStrip
from data_handler import DataHandler

device_counter = 0
data_handler = DataHandler()

cololight_strip = ColoStrip(ip=data_handler.get("STRIP_IP"), id=device_counter)
device_counter += 1

# owner_present variable tracks if owner's iPhone is connected to the specific network or not
# true -> owner connected to network, false -> owner not connected
owner_present = False

# active variable tracks if system should commit changes to real world, eg if checks have to be done
active = True
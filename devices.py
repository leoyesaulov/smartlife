from colo_strip import ColoStrip
from data_handler import DataHandler

device_counter = 0
data_handler = DataHandler()

cololight_strip = ColoStrip(ip=data_handler.get("STRIP_IP"), id=device_counter)
device_counter += 1
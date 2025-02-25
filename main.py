from pycololight import PyCololight
from dotenv import load_dotenv
import os

load_dotenv()

strip = PyCololight(device="strip", host=os.getenv("STRIP_IP"), dynamic_effects=True)

strip.on = 25
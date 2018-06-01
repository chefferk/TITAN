import arcpy
import math
import numpy as np
from arcpy.sa import *

#---------- Functions ----------#
def log(text):
    arcpy.AddMessage(text)

def convert_wind(wind_direction):
    PI = np.pi

    # converting the wind direction form degrees to pi
    wind_rad = (int(wind_direction) / 180 ) * PI

    # low wind value
    wind_low = wind_rad - (PI / 2)

    # high wind value
    wind_high = wind_rad + (PI / 2)

    # convert back to degrees
    # TODO : don't know if this part is needed
    wind_low = (wind_low * 180) / PI
    wind_high = (wind_high * 180) / PI

    # check that the values are between 0 - 360
    if wind_low <= 0:
        wind_low = wind_low + 360

    if wind_high > 360:
        wind_high = wind_high - 360

    # convert the values to percentages
    wind_low /= 360
    wind_high /= 360

    return wind_low, wind_high

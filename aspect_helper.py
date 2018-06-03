import arcpy
import math
import numpy as np
from arcpy.sa import *

#---------- Functions ----------#
def log(text):
    arcpy.AddMessage(text)

def convert_wind(wind_direction):
    log("----- Convert wind -----")
    # converting the wind direction form degrees to pi
    wind_rad = (int(wind_direction) / 180 ) * np.pi
    log(wind_rad)

    # low wind value
    wind_low = wind_rad - (np.pi / 2)
    log(wind_low)

    # high wind value
    wind_high = wind_rad + (np.pi / 2)
    log(wind_high)

    # convert back to degrees
    # TODO : don't know if this part is needed
    wind_low = (wind_low * 180) / np.pi
    log(wind_low)
    wind_high = (wind_high * 180) / np.pi
    log(wind_high)

    # check that the values are between 0 - 360
    if wind_low <= 0:
        log("YUP")
        wind_low = wind_low + 360
        log(wind_low)

    if wind_high > 360:
        log("Yes")
        wind_high = wind_high - 360
        log(wind_high)

    # convert the values to percentages
    wind_low /= 360
    log(wind_low)
    wind_high /= 360
    log(wind_high)
    log("----------")

    return wind_low * 100, wind_high * 100


def aspect_face():
    # create empty list
    aspect_faces = []

    # length * height
    aspect_faces.append(bb_lengths[0] * max_elevations[0])

    return aspect_faces


# take the aspect face area and multiply it by the width to get the volume of the object.
def volume():
    # create empty list
    volumes = []

    # volume = max_elevation * width * length
    volumes.append(bb_lengths[0] * max_elevations[0] * bb_widths[0])

    return volumes

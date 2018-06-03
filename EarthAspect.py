# File: EathAspect.py
# Title: Summer 2018 Titan research
# Desciption: This script will take objects in dune fields and find the aspect
#             face of the object and the width. This will all be based on the
#             wind direction.
# Authors: Weston Marek - wmarek19@tamu.edu
#          Keaton Cheffer - chefferk@tamu.edu
# Requirements: Spatial Analyst Extension

# Import system modules
import os
import sys
import arcpy
from arcpy import env
from arcpy.sa import *
import numpy as np
from aspect_helper import *

# DEBUG
debug = True

# Set environment settings
env.workspace = arcpy.GetParameterAsText(0)
env.overwriteOutput = True

# raster DEM
in_DEM = arcpy.GetParameterAsText(1)

# shape file
in_object = arcpy.GetParameterAsText(2)

# wind direction in degrees (0-360)
wind_direction = arcpy.GetParameterAsText(3)

# DEBUG
if debug:
    arcpy.AddMessage("\nWorkspace: {0} \n{1} \n" .format(env.workspace, type(env.workspace)))
    arcpy.AddMessage("in_DEM: {0} \n{1} \n" .format(in_DEM, type(in_DEM)))
    arcpy.AddMessage("in_object: {0} \n{1} \n" .format(in_object, type(in_object)))
    arcpy.AddMessage("wind_direction: {0} \n{1} \n" .format(wind_direction, type(wind_direction)))
    log("--------------------------------------------------------------------------------")

# ---------------------- create the Aspect raster file ----------------------- #
# Set local variables
in_raster = in_DEM
method = "PLANER"
z_unit = "METER"

# NOTE: for some reason, Aspect only accepts 3 variables on some machines
if arcpy.CheckExtension("Spatial") == "Available":
    log("Checking out Spatial")
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")
    try:
        # Execute Aspect
        out_aspect_obj = Aspect(in_DEM, "PLANER", "METER")
    except Exception as e:
        log("Aspect failed...")
        # Execute Aspect
        out_aspect_obj = Aspect(in_DEM)
else:
    arcpy.AddError("Unable to get spatial analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

# Save the output
out_aspect = "aspect.tif"

# DEBUG
if debug:
    arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect_obj, type(out_aspect_obj)))

out_aspect_obj.save(out_aspect)

# DEBUG
if debug:
    arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect_obj, type(out_aspect_obj)))

# TODO: This is still hardcoded for my environment
# -------------------------- Generate Exclude Area --------------------------- #
in_DEM_parts = os.path.split(in_DEM)
in_DEM_file = in_DEM_parts[1][:-4]
output = "C:\Users\chefferk\Documents\ArcGIS\Default.gdb\\" + in_DEM_file + "_Generate"

log(output)

'''
arcpy.GenerateExcludeArea_management(out_aspect, output, "16_BIT", "HISTOGRAM_PERCENTAGE", "", "", "", "", "", "", "", "", "0", "50")


# --------- clip the aspect raster to the extent of just the object ---------- #
# Set local variables
inRaster = "C:\Users\chefferk\Documents\ArcGIS\Default.gdb\ASTGTM2_N17W012_dem_Generate"
inMaskData = DesertObject

# Execute ExtractByMask
outExtractByMask = ExtractByMask(inRaster, inMaskData)

# Save the output
outExtractByMask.save("extractmask.tif")


# ----------- find the max elevations from the DEM and the objects ----------- #
# maxElevation = zonalStatisticsAsTable(LocationDEM, field, DesertObject, maxElevation)

# Set local variables
inZoneData = DesertObject
zoneField = "ID"
inValueRaster = in_raster
outTable = "maxElevation.dbf"

# Execute ZonalStatisticsAsTable
max_elevation = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable)
arcpy.AddMessage("max_elevation: {0} \n{1} \n" .format(max_elevation, type(max_elevation)))

# TODO : given measurments are decimal degrees, we want meters
# ------------------- apply bounding box to the aspect face ------------------ #
# Create variables for the input and output feature classes
inFeatures = DesertObject
outFeatureClass = "boundingbox.shp"

# Use MinimumBoundingGeometry function to get a convex hull area for each cluster of trees which are multipoint features
arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatureClass, "RECTANGLE_BY_WIDTH", "NONE", "", True)

log("finished.")
log("--------------------------------------------------------------------------------")

# take the bounding box length and the height from the DEM to find the aspect face.
bb_lengths = []
bb_widths = []
max_elevations = []

for row in rows:
    # take out file values and put into a list
    bb_lengths = [].append(row.getValue("length"))

    # take out file values and put into a list
    max_elevations.append(row.getvalue("elevation"))

aspect_faces = aspect_face(bb_lengths, max_elevations)
volumes = volume(bb_lengths, bb_widths, max_elevations)
'''

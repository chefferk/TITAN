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
debug = False

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

# DEBUG
if debug:
    arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect_obj, type(out_aspect_obj)))

# Save the output
out_aspect = "aspect.tif"
out_aspect_obj.save(out_aspect)

# DEBUG
if debug:
    arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect_obj, type(out_aspect_obj)))

log("Aspect created.")

# TODO: This is still hardcoded for my environment
# -------------------------- Generate Exclude Area --------------------------- #
in_DEM_parts = os.path.split(in_DEM)
in_DEM_file = in_DEM_parts[1][:-4]
in_DEM_output = "C:\Users\chefferk\Documents\ArcGIS\Default.gdb\\" + in_DEM_file + "_Generate"

# DEBUG
if debug:
    arcpy.AddMessage("in_DEM_output: {0} \n{1} \n" .format(in_DEM_output, type(in_DEM_output)))

wind_low, wind_high = convert_wind(wind_direction)



# Set local variables
in_raster = out_aspect
out_raster = in_DEM_output
pixel_type = "16_BIT"
generate_method = "HISTOGRAM_PERCENTAGE"
percentage_high = str(wind_low)
percentage_low = str(wind_high)

log(wind_low)
log(wind_high)

# Execute Generate Exclude Area
arcpy.GenerateExcludeArea_management(in_raster, out_raster, pixel_type, generate_method, "", "", "", "", "", "", "", "", percentage_low, percentage_high)

log("Generated Exclude Area.")

# --------- clip the aspect raster to the extent of just the object ---------- #
# Set local variables
in_raster = in_DEM_output
in_mask_data = in_object

# Execute Extract By Mask
out_extract_by_mask_obj = ExtractByMask(in_raster, in_mask_data)

# DEBUG
if debug:
    arcpy.AddMessage("out_extract_by_mask_obj: {0} \n{1} \n" .format(out_extract_by_mask_obj, type(out_extract_by_mask_obj)))

# Save the output
out_extract_by_mask = "extractMask.tif"
out_extract_by_mask_obj.save(out_extract_by_mask)

# DEBUG
if debug:
    arcpy.AddMessage("out_extract_by_mask_obj: {0} \n{1} \n" .format(out_extract_by_mask_obj, type(out_extract_by_mask_obj)))

log("Extracted mask created.")

# ----------- find the max elevations from the DEM and the objects ----------- #
# Set local variables
in_zone_data = in_object
zone_field = "ID"
in_value_raster = in_DEM
out_table = "maxElevation.dbf"

# Execute ZonalStatisticsAsTable
max_elevation = ZonalStatisticsAsTable(in_zone_data, zone_field, in_value_raster, out_table)

# DEBUG:
if debug:
    arcpy.AddMessage("max_elevation: {0} \n{1} \n" .format(max_elevation, type(max_elevation)))

log("Max elevation table created.")

# TODO : given measurments are decimal degrees, we want meters
# ------------------- apply bounding box to the aspect face ------------------ #
# Set local variables
in_features = in_object
out_feature_class = "boundingbox.shp"
geometry_type = "RECTANGLE_BY_WIDTH"
group_option = "NONE"
group_field = ""
mbg_fields_option = True

# Use MinimumBoundingGeometry function to get a convex hull area for each cluster of trees which are multipoint features
arcpy.MinimumBoundingGeometry_management(in_features, out_feature_class, geometry_type, group_option, group_field, mbg_fields_option)

log("Bounding box created.")

log("Finished.")
log("--------------------------------------------------------------------------------")
'''
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

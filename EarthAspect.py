# This is the python code for the Summer 2018 Titan research
# This code will take objects in dune fields and find the aspect face of the object and the width. This will all be based on the wind direction.

import arcpy
from aspect_helper import *
import math
import numpy as np
from arcpy.sa import *

# setting the workspace in the toolbox
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.AddMessage("\nWorkspace: {0} \n{1} \n" .format(arcpy.env.workspace, type(arcpy.env.workspace)))

LocationDEM = arcpy.GetParameterAsText(1)
arcpy.AddMessage("LocationDEM {0} \n{1} \n" .format(LocationDEM, type(LocationDEM)))

DesertObject = arcpy.GetParameterAsText(2)
arcpy.AddMessage("DesertObject: {0} \n{1} \n" .format(DesertObject, type(DesertObject)))

wind_direction = arcpy.GetParameterAsText(3)
arcpy.AddMessage("wind_direction: {0} \n{1} \n" .format(wind_direction, type(wind_direction)))

log("--------------------------------------------------------------------------------")
in_raster = "ASTGTM2_N17W012_dem.tif"

# create the Aspect raster data sheet
out_aspect = Aspect(in_raster)
arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect, type(out_aspect)))

arcpy.env.overwriteOutput = True
out_aspect.save("aspect.tif")
arcpy.AddMessage("out_aspect: {0} \n{1} \n" .format(out_aspect, type(out_aspect)))

# TODO : use commandline params
temp = "aspect.tif"
output = "C:\Users\chefferk\Documents\ArcGIS\Default.gdb\ASTGTM2_N17W012_dem_Generate"

arcpy.GenerateExcludeArea_management(temp, output, "16_BIT", "HISTOGRAM_PERCENTAGE", "", "", "", "", "", "", "", "", "0", "50")


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

# ------------------- apply bounding box to the aspect face ------------------ #
# Create variables for the input and output feature classes
inFeatures = DesertObject
outFeatureClass = "boundingbox.shp"

# Use MinimumBoundingGeometry function to get a convex hull area for each cluster of trees which are multipoint features
arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatureClass, "RECTANGLE_BY_WIDTH")

log("finished.")
log("--------------------------------------------------------------------------------")
# take the bounding box length and the height from the DEM to find the aspect face.

# list of the field named length in the bounding-box layer
boundingbox_length_list = []

# list of the field named elevation in the maxElevation layer
maxElevation_elevation_list = []

# list of the field named width in the bounding-box layer
boundingbox_width_list = []


'''
for row in rows:
    # take out file values and put into a list
    boundingbox_length_list.append(row.getValue("length"))

    # take out file values and put into a list
    maxElevation_elevation_list.append(row.getvalue("elevation"))

aspectFace_L = []
i = 0
# multiply the length by the height
while 1 >= i:
    aspectFace_L.append(boundingbox_length_list[i] * maxElevation_elevation_list[i])
    i += 1

# take the aspect face area and multiply it by the width to get the volume of the object.
Volume_L = []
i = 0
# this is the math multiplying the length by the height by the width
while 1 >= i:
    Volume_L.append(boundingbox_length_list[i] * maxElevation_elevation_list[i] * boundingbox_width_list[i])
    i += 1
'''

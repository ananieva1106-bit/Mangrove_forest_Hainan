# Importing packages
import os
import rasterio
import pandas as pd

# Importing the functions
from MangroveWatch import index_calculation
from MangroveWatch import time_slider_maps
from MangroveWatch import landsat_function

# Creation of directories
# source : exercice 10 solution
if not os.path.exists("data"):
    os.mkdirs("data")

if not os.path.exists("temp"):
    os.mkdirs("temp")

if not os.path.exists("output"):
    os.mkdirs("output")

### PREPARATION OF DATA ###

# Downloading the raster from landsat
# instruction to put the shapefile : in the README

years = [1996, 2003, 2010, 2016, 2020]

# Specifying the parameters
bbox =
bands = ["Red", "NIR", "SWIR"]
crs = 
output_dir = "data/landsat_data"
n_scenes =

for year in years:
    landsat_function.landsat_download(year, bbox, bands, crs, output_dir, n_scenes)


### CALCULATION OF THE INDEXES ###

NDVI_paths = []
NDMI_paths = []
for year in years:
    # extract the right tif file for the year 

    SWIR = rasterio.open(f"swir16_{year}.tif")
    NIR = rasterio.open(f"nir08_{year}.tif")
    Red = rasterio.open(f"red_{year}.tif")

    # Calculate the indexes
    NDVI_paths.append(index_calculation.calc_NDVI(NIR, Red, year))
    NDMI_paths.append(index_calculation.calc_NDMI(NIR, SWIR, year))

# df_NDVI = pd.DataFrame({'year' : years, 'path' : NDVI_paths})
# df_NDMI = pd.DataFrame({'year' : years, 'path' : NDMI_paths})

### CREATION OF THE TIME SLIDER ###
time_slider_maps.time_slider_raster(years, NDVI_paths)
time_slider_maps.time_slider_raster(years, NDMI_paths)
# Importing packages
import os
import rasterio
import pandas as pd

# Importing the functions
#from MangroveWatch import index_calculation
#from MangroveWatch import time_slider_maps
from MangroveWatch import landsat_download
from MangroveWatch import raster_masking_to_vector

# Creation of directories
# source : exercice 10 solution
if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data/landsat_data"):
    os.mkdir("data/landsat_data")

if not os.path.exists("temp"):
    os.mkdir("temp")

if not os.path.exists("output"):
    os.mkdir("output")

### PREPARATION OF DATA ###

# Downloading the raster from landsat
# instruction to put the shapefile : in the README

years = [1996, 2003, 2010, 2016, 2020]

# Specifying the parameters
bbox = (108.506470, 18.151072, 111.088257, 20.190035)
bands = ["red", "nir08", "swir16"]
crs = "EPSG:32649"
output_dir = "data/landsat_data"
n_scenes = 3

for year in years:
    #landsat_download.landsat_download(year, bbox, bands, crs, output_dir, n_scenes)

    # mask the raster to the extent of the mangrove
    # raster_masking_to_vector.mask_raster_to_vector(year, bbox)
    # raster_masking_to_vector.extent_raster(year, bbox) # trying to build map with timeslider using the vector data instead


### CALCULATION OF THE INDEXES ###

 NDVI_paths = []
 NDMI_paths = []
 for year in years:
#    swir, nir, red = index_calculation.extract_bands(year) 

#     # Calculate the indexes
#     NDVI_paths.append(index_calculation.calc_NDVI(nir, red, year))
#     NDMI_paths.append(index_calculation.calc_NDMI(nir, swir, year))

# # df_NDVI = pd.DataFrame({'year' : years, 'path' : NDVI_paths})
# # df_NDMI = pd.DataFrame({'year' : years, 'path' : NDMI_paths})

# ### CREATION OF THE TIME SLIDER ###
# time_slider_maps.time_slider_raster(years, NDVI_paths)
# time_slider_maps.time_slider_raster(years, NDMI_paths)
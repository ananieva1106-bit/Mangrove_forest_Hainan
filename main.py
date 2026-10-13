# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, october 2026
# This script is licensed under the MIT License
# Sources are reference throughout the script

# Importing packages
import os
import rasterio
import pandas as pd
import matplotlib.pyplot as plt

# Importing the functions
from MangroveWatch import landsat_download
from MangroveWatch import raster_masking_to_vector
from MangroveWatch import index_calculation
from MangroveWatch import plot
from MangroveWatch import map_dash

# Creation of directories
# source : exercice 10 solution
if not os.path.exists("data/vector"):
    raise FileNotFoundError("Data/vector subdirectories not found. See README.md: run pixi task mangrovesdownload first...")

if not os.path.exists("data/landsat_data"):
    os.mkdir("data/landsat_data")

if not os.path.exists("output"):
    os.mkdir("output")

# Defining the years of interest
years = [1996, 2003, 2010, 2016, 2020]

# Defining area of interest
bbox = (108.506470, 18.151072, 111.088257, 20.190035)

### DOWNLOADING THE DATA ###

# Downloading the raster from landsat
# Specifying the parameters
bands = ["red", "nir08", "swir16"]
crs = "EPSG:32649"
output_dir = "data/landsat_data"
n_scenes = 3

for year in years:
    landsat_download.landsat_download(year, bbox, bands, crs, output_dir, n_scenes)
 

## PREPARATION OF DATA ###
# Masking the data 

for year in years:
    # mask the raster to the extent of the mangrove
    raster_masking_to_vector.mask_raster_to_vector(year, bbox)

### CALCULATION OF THE INDEXES ###

NDVI_paths = []
NDMI_paths = []
frag_ratio = []
for year in years:
    swir, nir, red, meta = index_calculation.extract_bands(year) 

    # Calculate the indexes
    NDVI_paths.append(index_calculation.calc_NDVI(nir, red, year, meta))
    NDMI_paths.append(index_calculation.calc_NDMI(nir, swir, year, meta))

    # Extract degree of fragmentation of mangrove forests (edge to area ratio) values as table 
    frag_ratio.append(index_calculation.fragm_index(year, bbox))

# Putting the frag_ratio data into a table (as alternative plotting option)
df_frag = pd.DataFrame({'year' : years, 'fragmentation ratio' : frag_ratio})

# Plotting of the degree of fragmentation development over years
title = "Degree of fragmentation of mangrove forests in Hainan"
y_label = "Edge-to-area ratio of mangrove forests"
caption = ("Degree of fragmentation is expressed through the edge-to-area ratio. "
    "The ratio is calculated for the given years and mangrove forest extent "
    "across Hainan Island.")

plot.development_plot(years, frag_ratio, title, caption, y_label)

### VISUALIZATION ###
from MangroveWatch import map_dash
map_dash.run_dashboard()
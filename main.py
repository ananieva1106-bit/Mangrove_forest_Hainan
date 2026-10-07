# Importing packages
import os

# Importing the functions
from MangroveWatch import index_calculation
from MangroveWatch import prepare_data

# Creation of directories
# source : exercice 10 solution
if not os.path.exists("data"):
    os.mkdirs("data")

if not os.path.exists("temp"):
    os.mkdirs("temp")

if not os.path.exists("output"):
    os.mkdirs("output")

# Preparation of data

# raster downloading
# instruction to put the shapefile : in the README

# Calculating the indexes
years = [1990, 1996, 2003, 2010, 2016, 2020]

for year in years:
    # extract the right tif file for the year 
    SWIR, NIR, Red = index_calculation.extract_bands_landsat(year)

    # Calculate the indexes
    index_calculation.calc_NDVI(NIR, Red, year)
    index_calculation.calc_NDMI(NIR, SWIR, year)
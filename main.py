# Importing packages
import os
import rasterio
import pandas as pd
import matplotlib.pyplot as plt

# Importing the functions
from MangroveWatch import landsat_download
# from MangroveWatch import mangroves_download
from MangroveWatch import raster_masking_to_vector
from MangroveWatch import index_calculation


# Creation of directories
# source : exercice 10 solution
if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data/landsat_data"):
    os.mkdir("data/landsat_data")

if not os.path.exists("data/vector"):
    os.mkdir("data/vector")

if not os.path.exists("temp"):
    os.mkdir("temp")

if not os.path.exists("output"):
    os.mkdir("output")

### PREPARATION OF DATA ###

# Downloading the mangroves vector data through url: instruction to get the shapefile: please see the README.md 

# Downloading the raster from landsat
# Defining the years of interest
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
    raster_masking_to_vector.mask_raster_to_vector(year, bbox) 
    # raster_masking_to_vector.extent_raster(year, bbox) # trying to build map with timeslider using the vector data instead # not used anymore


### CALCULATION OF THE INDEXES ###

NDVI_paths = []
NDMI_paths = []
Frag_ratio = []
for year in years:
    swir, nir, red, meta = index_calculation.extract_bands(year) 

    # Calculate the indexes
    # NDVI_paths.append(index_calculation.calc_NDVI(nir, red, year, meta))
    # NDMI_paths.append(index_calculation.calc_NDMI(nir, swir, year, meta))

    # Extract degree of fragmentation of mangrove forests (edge to area ratio) values as table 
    Frag_ratio.append(index_calculation.fragm_index(year, bbox))

df_frag = pd.DataFrame({'year' : years, 'fragmentation ratio' : Frag_ratio})
plt.plot(Frag_ratio, years) 
plt.savefig("output/Fragm_ratio_table.png")
plt.show()
# df_NDMI = pd.DataFrame({'year' : years, 'path' : NDMI_paths})

# ### CREATION OF THE TIME SLIDER ###
# time_slider_maps.time_slider_raster(years, NDVI_paths)
# time_slider_maps.time_slider_raster(years, NDMI_paths)
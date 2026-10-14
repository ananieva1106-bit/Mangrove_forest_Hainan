# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, October 2026
# This script is licensed under the MIT License
# Sources are referenced throughout the script

# Importing the packages
import os
import numpy as np
import pystac_client
import planetary_computer
import odc.stac
import rasterio
import numpy as np
import xarray as xr

"""
    Extracts all Landsat Collection 2 Level 2 scenes as a list for a set year, region, and bands 
    between 1st of December (from prev year) to end of March.
    Of all scenes found, selects n-amount of least cloudy scenes, applies cloud mask,
    creates multi-band composite of selected and cloudmasked scenes and writes it to disk.
    :param year = year of interest, bbox = Lat/Long coordinates of region of interest, 
    crs = coordinate reference system, output_dir = relative folder path for writing the final output to
    n_scenes = number of least cloudy scenes to search for for creating the composite
"""
# vars
year = (2003)
bbox = (108.506470, 18.151072, 111.088257, 20.190035)
bands = ["red", "nir08", "swir16"]
crs = "EPSG:32649"
output_dir = "data/landsat_data"

# Connects to Microsofts Planetary Computer
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
    # Loads all found scenes as list 
    # Source: https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac/
items = list(catalog.search(
    collections=["landsat-c2-l2"],
    bbox=bbox,
    datetime=f"{year-1}-12-01/{year}-03-30",
    query={"platform": {"eq": "landsat-5" if year < 2013 else "landsat-8"}, 
    "eo:cloud_cover": {"lt": 50}},
).items())

# Loading all found scenes iusing odc.stac 
# Source: https://discourse.pangeo.io/t/comparing-odc-stac-load-and-stackstac-for-raster-composite-workflow/4097
stack = odc.stac.load(
    items, 
    bands=bands + ["qa_pixel"], 
    bbox=bbox,
    crs=crs, 
    resolution=100,
    groupby="solar_day"
)

# Create cloud mask
# Source: https://gis.stackexchange.com/questions/470283/mask-clouds-and-cloud-shadow-on-landsat-8-images-using-google-earth-engine
# 1 << 2 for cirrus, 1 << 3 for cloud, 1 << 4 for cloud shadow
all_clouds = (1 << 2) | (1 << 3) | (1 << 4)
# qa_pixel nodata value is 1 and should also be removed (Source: https://docs.digitalearthafrica.org/en/latest/data_specs/Landsat_C2_SR_specs.html)
cl_mask = (stack["qa_pixel"] & all_clouds != 0)
# Masking out the cloud mask
# Source: (Source: https://earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/remove-clouds-from-landsat-data/)
stack = stack.where(~cl_mask)

# Compute median composite
layers = []
for band in bands:
    a = stack[band].values.astype("float32")
    # Convert standard Landsat reflectance band nodata value 0 to NaN & convert raw DS to scaled reflectance value
    # Source: https://docs.digitalearthafrica.org/en/latest/data_specs/Landsat_C2_SR_specs.html
    a[a == 0] = np.nan 
    a = (a * 0.0000275) - 0.2
    # Source: https://gis.stackexchange.com/questions/467543/create-multiband-raster-in-python-from-x-y
    layers.append(np.nanmedian(a, axis=0))
arr = np.stack(layers).astype("float32")

# Source: https://gis.stackexchange.com/questions/467543/create-multiband-raster-in-python-from-x-y
# Create metadata profile
profile = {
    "driver": "GTiff",
    "dtype": "float32",
    "nodata": np.nan,
    "crs": crs,
    "transform": stack.odc.geobox.affine,
    "count": arr.shape[0],
    "height": arr.shape[1],
    "width": arr.shape[2],
}
    
# Write file
with rasterio.open(f"{output_dir}/{year}.tif", "w", **profile) as dst:
    dst.write(arr)
    dst.descriptions = bands
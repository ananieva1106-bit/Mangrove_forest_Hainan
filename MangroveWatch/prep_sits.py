# Developement of Mangrove Forests on Hainan Island
# Geoscripting GRS 33806
# Group Project by Roxane Marguerat, Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger
# Group proect challenge n.9

# In this script, the satellite data is retrieved by using sits package

# Source: https://sits.readthedocs.io/en/latest/tutorials/colab_sits_ex01.html
from sits import sits, export
from datetime import datetime
import pyproj
from shapely.geometry import box
from shapely.ops import transform

# Define a bounding box
bbox_4326 = (108.506470, 18.151072, 111.088257, 20.190035)

# Downloading the data
# Selecting years
years = [1990, 1996, 2003, 2010, 2016, 2020]
cubes = {}

for year in years:
    if year < 2013:
        platform = 'landsat-5'   # 1984-2013
    else:
        platform = 'landsat-8'   # since 2013

    # instance of the class sits.StacAttack()
    ts = sits.StacAttack(provider='mpc', collection='landsat-c2-l2', bands=['red', 'nir', 'swir16'])
    
    # search of items based on bbox coordinates and time interval criteria
    ts.searchItems(bbox_4326,
                   date_start=datetime(year, 1, 1),
                   date_end=datetime(year, 1, 31),
                   query={"platform": {"eq": platform}})

    # load of the time series
    ts.loadCube(bbox_utm, resolution=30, crs_out=32649)

    # also need to mask and gap fill the masked pixels

    cubes[year] = ts

    # Export each year
    for year, ts in cubes.items():
    ts.to_nc('output')
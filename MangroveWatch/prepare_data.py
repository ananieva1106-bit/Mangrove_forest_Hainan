### Preparing data code block: Elmo van den Beld

# Load packages
import shapely.geometry
import geopandas as gpd
import os


# Load a mangrove shapefiles
def loadMangroves(filepath: str):
    mangroveTest = gpd.read_file(filepath)
    print(mangroveTest.head)
    return mangroveTest

# Check crs of shapefile

# Clip mangrove vector data using bounding box coordinates for Hainan
groveClip 

### end of code block

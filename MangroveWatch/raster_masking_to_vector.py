# Developement of Mangrove Forests on Hainan Island
# Geoscripting GRS 33806
# Group Project by Roxane Marguerat, Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger
# Group proect challenge n.9

# In this script, the satellite raster data is masked to the vector data, to only keep data that is within the area of interest 

# inverse = true

# Source: https://gis.stackexchange.com/questions/444062/clipping-raster-geotiff-with-a-vector-shapefile-in-python

# Importing the packages neeed for the function
import rasterio
from rasterio import mask
import geopandas as gpd

# handling non data needed? 

# define function to create a mask of raster to the vector data, using rasterio

def mask_raster_to_vector(year_list, bbox)
    """ 
    Function that masks raster data to a shapefile. The function takes a year of interest as input as well as a bbox to define the area of interest.  
    """
    # specifying the directories for data, that contain the year of interest
    input_shps = [f'data/mangroves_china/mangrove{year}.shp' for year in year_list]
    input_shp = f"data/vector/mangrove{year}.shp"
    input_raster = f"data/raster/{year}.tif" # needs to be adapted to actual path name still. 
    output_raster = f"data/raster/landsat_mask{year}.tif"

    # read the vector data
    mangrove_shp = gpd.read_file(input_shp, bbox)

    # open the raster data and masking it to vector geometry
    with rasterio.open(input_raster) as src:
        mangrove_shp=mangrove_shp.to_crs(src.crs) # bringing vector and raster data into same projection 
        out_raster, out_transform=mask(src,mangrove_shp.geometry,crop=True, inverse=True)
        out_meta=src.meta.copy() # copy metadata from the original raster data

    # updating meta data
    # source: https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
    out_meta.update({
        "driver":"Gtiff",
        "height":out_image.shape[1], #this needs to be checked once running with actual data!  
        "width":out_image.shape[2],
        "transform":out_transform
    })

    # open a new raster file and write the masked data to it          
    with rasterio.open(output_raster,'w',**out_meta) as dst:
        dst.write(out_raster)



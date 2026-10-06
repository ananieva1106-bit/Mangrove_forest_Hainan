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

def mask_raster_to_vector(year_list, bbox):
    """ 
    Function that masks raster data to a shapefile. The function takes a year of interest as input as well as a bbox to define the area of interest.  
    """
    # Load in vectors as GPD
    for year in year_list:
        # specifying the directories for data, that contain the year of interest
        vectorGPDs = {year: gpd.read_file(f'data/vector/mangrove{year}.shp', bbox=bbox)}
        input_rasters_fp = [f'data/raster/rastername{year}.tif'] # Add actual path name
        output_rasters_fp = [f"data/raster/landsat_mask{year}.tif"]


    # open the raster data and masking it to vector geometry
    for raster in input_rasters_fp:
        with rasterio.open(raster) as src:
            mangrove_shp=mangrove_shp.to_crs(src.crs) # bringing vector and raster data into same projection 
            out_image, out_transform=mask(src,mangrove_shp.geometry,crop=True)
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
    with rasterio.open(output_rasters_fp,'w',**out_meta) as dst:
        dst.write(out_image)
    
    



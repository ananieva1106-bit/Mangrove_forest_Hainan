# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, october 2026
# This script is licensed under the MIT License
# Sources are reference throughout the script

### In this script, the satellite raster data is masked to the vector data, 
### to only keep data that is within the area of interest 

# General source used: https://gis.stackexchange.com/questions/444062/clipping-raster-geotiff-with-a-vector-shapefile-in-python

# Importing the packages
import rasterio
from rasterio.mask import mask
import geopandas as gpd


def mask_raster_to_vector(year, bbox):
    """ 
    Masks raster data on the extent of a shapefile. 
    :param year of interest and bbox of the area of interest 
    """

    # Loading in vectors as GPD
    mangrove_shp = gpd.read_file(f'data/vector/Mangrove Dynamics in China/mangrove{year}.shp', bbox=bbox)

    # Specifying the file path for the rasters
    input_raster_fp = f'data/landsat_data/{year}.tif'
    output_raster_fp = f"data/landsat_data/mask_{year}.tif"

    with rasterio.open(input_raster_fp) as src:
        mangrove_shp = mangrove_shp.to_crs(src.crs) # bringing vector and raster data into same projection 
        out_image, out_transform = mask(src,mangrove_shp.geometry,crop = True) # source : tutorial 11
        out_meta = src.meta.copy() # copying metadata from the original raster data

    # Updating meta data (Source: https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html)
    out_meta.update({
        "driver":"Gtiff",
        "height":out_image.shape[1],
        "width":out_image.shape[2],
        "transform":out_transform
    })

    # Opening a new raster file and writing the masked data into it          
    with rasterio.open(output_raster_fp,'w',**out_meta) as dst:
        dst.write(out_image)

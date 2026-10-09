# Developement of Mangrove Forests on Hainan Island
# Geoscripting GRS 33806
# Group Project by Roxane Marguerat, Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger
# Group proect challenge n.9

# In this script, the satellite raster data is masked to the vector data, to only keep data that is within the area of interest 

# inverse = true

# Source: https://gis.stackexchange.com/questions/444062/clipping-raster-geotiff-with-a-vector-shapefile-in-python

# Importing the packages neeed for the function
from bqplot import shape
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

# handling non data needed? 

# define function to create a mask of raster to the vector data, using rasterio

def mask_raster_to_vector(year, bbox):
    """ 
    Function that masks raster data to a shapefile. The function takes a year of interest as input as well as a bbox to define the area of interest.  
    """
    # Load in vectors as GPD
    mangrove_shp = gpd.read_file(f'data/vector/mangrove{year}.shp', bbox=bbox)

    # Specifying the file path for the rasters
    input_raster_fp = f'data/landsat_data/{year}.tif'
    output_raster_fp = f"data/landsat_data/mask_{year}.tif"


    with rasterio.open(input_raster_fp) as src:
        mangrove_shp = mangrove_shp.to_crs(src.crs) # bringing vector and raster data into same projection 
        out_image, out_transform = mask(src,mangrove_shp.geometry,crop = True) # source : tutorial 11
        out_meta = src.meta.copy() # copy metadata from the original raster data

    # updating meta data
    # source: https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
    out_meta.update({
        "driver":"Gtiff",
        "height":out_image.shape[1], #this needs to be checked once running with actual data!  
        "width":out_image.shape[2],
        "transform":out_transform
    })

    # open a new raster file and write the masked data to it          
    with rasterio.open(output_raster_fp,'w',**out_meta) as dst:
        dst.write(out_image)

# def extent_raster(year, bbox):

#     # Specifyfing file path for the input vector and output raster
#     mangrove_shp = gpd.read_file(f'data/vector/mangrove{year}.shp', bbox)
#     input_raster_fp = f'data/landsat_data/mask_{year}.tif'
#     output_raster_fp = f"data/extent_{year}.tif"

#     with rasterio.open(input_raster_fp) as src:
#         array = src.read(1)
#         out_meta = src.meta.copy() # copying the meta data
#         transform = src.transform
       
#     out_meta.update(count=1, dtype="uint8", nodata=0)
    
#     shapes = (
#         (geom, 1)
#      for geom in mangrove_shp.geometry
#      #if geom is not None and not geom.is_empty
#     )

#     extent_array = rasterio.features.rasterize(shapes, transform = transform, out_shape = array.shape)


#     with rasterio.open(output_raster_fp,'w',**out_meta) as dst: # writing the tif file of the extent
#         dst.write(extent_array, 1)




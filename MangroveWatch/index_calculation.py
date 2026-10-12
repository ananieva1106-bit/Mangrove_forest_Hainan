# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, october 2026
# This script is licensed under the MIT License
# Sources are reference throughout the script

# This script implements functions to calculate of indexes on raster bands and vector shapefiles

# Importing the packages
import rasterio
import geopandas as gpd

def extract_bands(year):
    """
    Extracts the individual swir, nir and red bands out of the raster
    Extracts the meta data of the raster.
    :param year = year of the raster image.
    """
    input_raster_fp = f"data/landsat_data/mask_{year}.tif"

    # Extracting the bands by calling them in the order defined in raster downloading function.
    with rasterio.open(input_raster_fp) as src:
        swir = src.read(3)
        nir = src.read(2)
        red = src.read(1)

        # Extracting the meta data to use to write raster files in index calculations.
        out_meta = src.meta.copy()

    return swir, nir, red, out_meta




def calc_NDVI(NIR, Red, year, meta):
    """
    Calculates the NDVI (normalized difference vegetation index), creates a tif file and returns its path
    :param NIR = near infrared band, Red = red band, year = year of raster image, meta = metadata from raster image
    """
    NDVI = (NIR - Red)/(NIR + Red)

    # Creating the file path
    path = f"output/NDVI_{year}.tif"

    # Saving the NDVI as a raster
    with rasterio.open(path, 'w', **meta) as file:
        file.write(NDVI.astype(rasterio.float32), 1)
    
    return path
    

def calc_NDMI(NIR, SWIR, year, meta):
    """
    Calculate the NDMI (normalized difference moisture index), creates a tif file and returns its path
    :param NIR = near infrared band, SWIR = short-wave infrared band, year = year of satellite image, meta = metadata from raster image
    """
    NDMI = (NIR - SWIR)/(NIR + SWIR)

    # Creating the file path
    path = f"output/NDMI_{year}.tif"

    # Saving the NDMI as a raster
    with rasterio.open(path, 'w', **meta) as file:
        file.write(NDMI.astype(rasterio.float32), 1)
    
    return path


def fragm_index(year, bbox):
    """
    Calculate the edge-to-area ratio as an indicator for fragmentation     
    :param year of the mangrove extent and bbox to read the vector file as geodataframe. 
    """
    # Opening the vector data containing mangrove extent as a geodataframe
    gdf = gpd.read_file(f"data/vector/Mangrove Dynamics in China/mangrove{year}.shp", bbox=bbox)

    # Bringing the data to a projection in meters to be able to run calculations with length and area
    gdf = gdf.to_crs("EPSG:32649")
    
    # Calculating the edge-to-area ratio for the mangrove forest extent, given a year
    ratios = gdf.geometry.length / gdf.geometry.area
    
    return ratios.mean()
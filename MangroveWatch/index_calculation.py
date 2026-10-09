import rasterio
import geopandas as gpd
from shapely import MultiPolygon

def extract_bands(year):
    """
    Extract the individual bands of the raster
    """
    input_raster_fp = f"data/landsat_data/mask_{year}.tif"
    with rasterio.open(input_raster_fp) as src:
        swir = src.read(3)
        nir = src.read(2)
        red = src.read(1)
        out_meta = src.meta.copy()

    return swir, nir, red, out_meta




def calc_NDVI(NIR, Red, year, meta):
    """
    Calculate the NDVI, normalized difference vegetation index
    :param NIR = near infrared band, Red = red band, year = year of satellite image
    """
    # NDVI = np.zeroes_like(NIR)
    NDVI = (NIR - Red)/(NIR + Red)

    path = f"temp/NDVI_{year}.tif"
    # Save the NDVI as a raster
    with rasterio.open(path, 'w', **meta) as file:
        file.write(NDVI.astype(rasterio.float32), 1)
    
    return path
    

def calc_NDMI(NIR, SWIR, year, meta):
    """
    Calculate the NDMI, normalized difference moisture index
    :param NIR = near infrared band, SWIR = short-wave infrared band, year = year of satellite image
    """
    NDMI = (NIR - SWIR)/(NIR + SWIR)

    path = f"temp/NDMI_{year}.tif"

    # Save the NDMI as a raster
    with rasterio.open(path, 'w', **meta) as file:
        file.write(NDMI.astype(rasterio.float32), 1)
    
    return path


# def fragm_index(year, bbox):
#     """
#     Calculate the edge-to-area ratio as an indicator for fragmentation
#     :param year to find corresponding vector layer of magrove extent
#     """

#     mangrove_shp = gpd.read_file(f'data/vector/mangrove{year}.shp', bbox)
#     #polygons_geoms = mangrove_shp.geoms

#     for feature in mangrove_shp:
#     #for polygon in polygons_geoms:
#         # source: https://gis.stackexchange.com/questions/122957/how-to-calculate-the-perimeter-of-the-polygon-using-python-programming
#         polygons = mangrove_shp[feature].geometry()
#         for polygon in polygons:
#             length = polygon.geometry.length() # perimeter of the polygon
#             area = polygon.geometry.area() # area of the polygon
#             polygon.ratio = length/area # edge-to-area ratio
#     # source: https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean    
#     mean_ratio = mangrove_extent.ratio.mean() # average of the ratio for all polygons
#     return mean_ratio

def fragm_index(year, bbox):
    """
    Calculate the edge-to-area ratio as an indicator for fragmentation     
    :param year to find corresponding vector layer of magrove extent and bbox to read the vector file as geodataframe. 
    """
    # opening the vector data containing mangrove extent as a geodataframe
    gdf = gpd.read_file(f"data/vector/mangrove{year}.shp", bbox=bbox)
    
    # bring the data to a projection in meters to be able to run calculations with length and area
    gdf = gdf.to_crs("EPSG:32649")
    
    # Calculating the edge-to-area ratio for the mangrove forest extent, given a year
    ratios = gdf.geometry.length / gdf.geometry.area
    
    return ratios.mean()
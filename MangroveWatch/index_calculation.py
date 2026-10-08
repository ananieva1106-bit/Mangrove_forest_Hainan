import rasterio

def extract_bands(year):
    """
    Extract the individual bands of the raster
    """
    input_raster_fp = f"data/landsat_data/mask_{year}.tif"
    with rasterio.open(input_raster_fp) as src:
        swir = src["swir16"]
        nir = src["nir08"]
        red = src["red"]

    return swir, nir, red




def calc_NDVI(NIR, Red, year):
    """
    Calculate the NDVI, normalized difference vegetation index
    :param NIR = near infrared band, Red = red band, year = year of satellite image
    """
    # NDVI = np.zeroes_like(NIR)
    NDVI = (NIR - Red)/(NIR - Red)

    #Copy metadata of one of the raster
    out_meta = NIR.meta 
    path = f"temp/NDVI_{year}.tif"
    # Save the NDVI as a raster
    with rasterio.open(path, 'w', **out_meta) as file:
        file.write(NDVI.astype(rasterio.float32))
    
    return path
    

def calc_NDMI(NIR, SWIR, year):
    """
    Calculate the NDMI, normalized difference moisture index
    :param NIR = near infrared band, SWIR = short-wave infrared band, year = year of satellite image
    """
    NDMI = (NIR - SWIR)/(NIR + SWIR)

    #Copy metadata of one of the raster
    out_meta = NIR.meta 
    path = f"temp/NDMI_{year}.tif"

    # Save the NDMI as a raster
    with rasterio.open(path, 'w', **out_meta) as file:
        file.write(NDMI.astype(rasterio.float32))
    
    return path


def fragm_index(mangrove_extent):
    """
    Calculate the edge-to-area ratio as an indicator for fragmentation
    :param vector layer of magrove extent
    """
    for feature in mangrove_extent:
        # source: https://gis.stackexchange.com/questions/122957/how-to-calculate-the-perimeter-of-the-polygon-using-python-programming
        length = feature.geometry().length() # perimeter of the polygon
        area = feature.geometry().area() # area of the polygon
        feature.ratio = length/area # edge-to-area ratio
    # source: https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean    
    mean_ratio = mangrove_extent.ratio.mean() # average of the ratio for all polygons
    return mean_ratio

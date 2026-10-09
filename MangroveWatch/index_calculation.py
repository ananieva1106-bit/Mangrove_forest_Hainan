import rasterio

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

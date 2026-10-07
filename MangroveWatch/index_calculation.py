def calc_NDVI(NIR, Red):
    """
    Calculate the NDVI, normalized difference vegetation index
    :param NIR = near infrared band, Red = red band
    source: Exercise 6 Geoscripting course
    """
    NDVI = (NIR - Red)/(NIR - Red)
    return NDVI

def calc_NDMI(NIR, SWIR):
    """
    Calculate the NDMI, normalized difference moisture index
    :param NIR = near infrared band, SWIR = short-wave infrared band
    source: Exercise 6 Geoscripting course
    """
    NDMI = (NIR - SWIR)/(NIR + SWIR)
    return NDMI

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

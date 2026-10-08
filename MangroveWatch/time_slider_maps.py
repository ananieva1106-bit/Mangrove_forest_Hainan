# importing the packages needed to create a map with timeslider
import pandas as pd
import leafmap.maplibregl as leafmap


def time_slider_raster(years, paths):
    """
    Function that creates a map visualization with time-slider throughout different years.
    : param dataframe that contains year column, name of raster files  as well as path to raster-files. 
    source: https://leafmap.org/maplibre/time_slider/ 
    """
    
    # years = df["year"].to_list() # creating a list of available years in gdf
    # years = [str(year) for year in years] # converting years column into string
    # images = df["path"].to_list()

    # creating a map with raster images and adding timeslider element for the five selected years
    map = leafmap.Map(projection="globe", sidebar_visible=True, layer_manager_expanded=False)
    map.add_basemap("OpensStreetMap")
    map.add_time_slider(
        paths, #images 
        labels=years,
        opacity=1,
        expanded=True,
        time_interval=1,
    )
    map
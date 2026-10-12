# Sources: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
# https://nbviewer.org/format/script/github/jupyter-widgets/ipyleaflet/blob/0.16.0/examples/Numpy.ipynb
# https://www.dash-leaflet.com/
# https://dash.plotly.com/component-argument-order
import os
import numpy as np
import rasterio
import geopandas as gpd
import matplotlib.colors
import matplotlib.cm as cm
from rasterio.warp import transform_bounds
from PIL import Image
from dash import Dash, dcc, html, Input, Output, callback, ctx
import dash_leaflet as dl

app = Dash()

# Create a subfolder called assets inside data because dash needs it to store the png images
os.makedirs("data/assets", exist_ok=True)

# Defining the areas of interest
areas_of_interest = {
    "area1": {
        "label": "Area 1",
        "bounds": [[19.848175, 110.291598], [20.116546, 110.677381]],
        "center": [19.954933, 110.477444],
        "zoom": 11,
    },
    "area2": {
        "label": "Area 2",
        "bounds": [[19.668592, 109.114837], [19.973400, 109.588499]],
        "center": [19.821290, 109.351420],
        "zoom": 11,
    },
    "area3": {
        "label": "Area 3",
        "bounds": [[19.393506, 110.663167], [19.653592, 110.965212]],
        "center": [19.489583, 110.767949],
        "zoom": 11,
    },
}

years = [1996, 2003, 2010, 2016, 2020]


# Source: https://nbviewer.org/format/script/github/jupyter-widgets/ipyleaflet/blob/0.16.0/examples/Numpy.ipynb
# Convert tif files to png
def tif_to_png_overlay(tif_path, png_path):
    """Convert a 3-band true color GeoTIFF into a PNG + lat/lon bounds for dl.ImageOverlay."""
    with rasterio.open(tif_path) as src:
        arr = src.read([1, 2, 3])  # red, nir08, swir16
        arr = np.clip(arr / np.nanpercentile(arr, 98) * 255, 0, 255).astype("uint8")
        arr = np.moveaxis(arr, 0, -1)
        Image.fromarray(arr).save(png_path)

        west, south, east, north = transform_bounds(src.crs, "EPSG:4326", *src.bounds)
        bounds = [[south, west], [north, east]]

    return bounds


# Source: https://matplotlib.org/stable/users/explain/colors/colormaps.html
def tif_to_png_singleband(tif_path, png_path, cmap_name, vmin, vmax):
    """Convert a single band raster (NDVI/NDMI) into a colored PNG + lat/lon bounds."""
    with rasterio.open(tif_path) as src:
        arr = src.read(1)
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
        cmap = cm.get_cmap(cmap_name)
        rgba = (cmap(norm(arr)) * 255).astype("uint8")
        Image.fromarray(rgba, mode="RGBA").save(png_path)

        west, south, east, north = transform_bounds(src.crs, "EPSG:4326", *src.bounds)
        bounds = [[south, west], [north, east]]

    return bounds


# Source: https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.to_json.html
# Load the mangrove shp files as gdf and convert to GeoJSON
def get_extent_geojson(year):
    """Load the mangrove extent shapefile for a given year, as GeoJSON for dl.GeoJSON."""
    gdf = gpd.read_file(f"data/vector/mangrove{year}.shp")
    return gdf.__geo_interface__


# Drawing the main map, centered on Hainan
app.layout = html.Div([
    dl.Map(
        id="map",
        center=[19.2, 109.8],
        zoom=7,
        children=[
            dl.TileLayer(),
            # Rectangles marking the three areas of interest
            dl.Rectangle(bounds=areas_of_interest["area1"]["bounds"], id="rect-area1"),
            dl.Rectangle(bounds=areas_of_interest["area2"]["bounds"], id="rect-area2"),
            dl.Rectangle(bounds=areas_of_interest["area3"]["bounds"], id="rect-area3"),
        ],
        style={'height': '60vh'},
    ),

    # Generating the necessary buttons
    html.Div([
        html.Button("Area 1", id="btn-area1", n_clicks=0),
        html.Button("Area 2", id="btn-area2", n_clicks=0),
        html.Button("Area 3", id="btn-area3", n_clicks=0),
        html.Button("Reset view", id="btn-reset", n_clicks=0),
    ]),

    # Source: https://dash.plotly.com/dash-core-components/radioitems
    # Toggle between #####true color, NDVI, NDMI, and mangrove extent
    dcc.RadioItems(
        options=[
            {'label': 'True Color', 'value': 'truecolor'},
            {'label': 'NDVI', 'value': 'ndvi'},
            {'label': 'NDMI', 'value': 'ndmi'},
            {'label': 'Mangrove Extent', 'value': 'extent'},
        ],
        value='truecolor',
        id='layer-toggle'
    ),

    # Adding the slider with the years
    # Source: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
    dcc.Slider(
        min(years), max(years), step=None, value=min(years),
        marks={str(year): str(year) for year in years},
        id='year-slider'
    ),
])


# Whenever the slider or the toggle changes, rebuild the map layers:
# base tiles, the three area rectangles, and the selected layer
@callback( # @callback makes dash interactive
    Output('map', 'children'),
    Input('year-slider', 'value'),
    Input('layer-toggle', 'value'))
# def update_map(selected_year, layer_choice):
    layers = [
        dl.TileLayer(),
        dl.Rectangle(bounds=areas_of_interest["area1"]["bounds"], id="rect-area1"),
        dl.Rectangle(bounds=areas_of_interest["area2"]["bounds"], id="rect-area2"),
        dl.Rectangle(bounds=areas_of_interest["area3"]["bounds"], id="rect-area3"),
    ]

    if layer_choice == "truecolor":
        raster_path = f"data/landsat_data/mask_{selected_year}.tif"
        png_path = os.path.join("data", "assets", f"truecolor_{selected_year}.png")
        bounds = tif_to_png_overlay(raster_path, png_path)
        layers.append(dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8))

    elif layer_choice == "ndvi":
        raster_path = f"temp/NDVI_{selected_year}.tif"
        png_path = os.path.join("data", "assets", f"ndvi_{selected_year}.png")
        bounds = tif_to_png_singleband(raster_path, png_path, "RdYlGn", vmin=-0.2, vmax=0.8)
        layers.append(dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8))

    elif layer_choice == "ndmi":
        raster_path = f"temp/NDMI_{selected_year}.tif"
        png_path = os.path.join("data", "assets", f"ndmi_{selected_year}.png")
        bounds = tif_to_png_singleband(raster_path, png_path, "YlGnBu", vmin=-0.5, vmax=0.5)
        layers.append(dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8))

    elif layer_choice == "extent":
        geojson = get_extent_geojson(selected_year)
        layers.append(dl.GeoJSON(data=geojson, id="extent-layer"))

    return layers
# has to be finished

# One callback per zoom button (each just flies the map to its own area)
@callback(
    Output("map", "viewport"),
    Input("btn-area1", "n_clicks"),
    Input("btn-area2", "n_clicks"),
    Input("btn-area3", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def zoom_to_area(n1, n2, n3, n_reset):
    triggered = ctx.triggered_id
    mapping = {"btn-area1": "area1", "btn-area2": "area2", "btn-area3": "area3"}
    if triggered in mapping:
        a = areas_of_interest[mapping[triggered]]
        return dict(center=a["center"], zoom=a["zoom"], transition="flyTo")
    return dict(center=[19.2, 109.8], zoom=7, transition="flyTo")


# Start the dash server
if __name__ == '__main__':
    app.run(debug=True)
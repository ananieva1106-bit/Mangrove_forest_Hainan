# Main sources: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
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
        "zoom": 10.5,
    },
    "area2": {
        "label": "Area 2",
        "bounds": [[19.668592, 109.114837], [19.973400, 109.588499]],
        "center": [19.821290, 109.351420],
        "zoom": 10.5,
    },
    "area3": {
        "label": "Area 3",
        "bounds": [[19.393506, 110.663167], [19.653592, 110.965212]],
        "center": [19.489583, 110.767949],
        "zoom": 10.5,
    },
}


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


# Source: https://geopandas.org/en/latest/docs/reference/api/geopandas.GeoDataFrame.__geo_interface__.html
# Load the mangrove shp files as gdf and convert to GeoJSON
def get_extent_geojson(year):
    """Load the mangrove extent shapefile for a given year, as GeoJSON for dl.GeoJSON."""
    gdf = gpd.read_file(f"{VECTOR_DIR}/mangrove{year}.shp")
    return gdf.__geo_interface__


# Sources: https://www.dash-leaflet.com/
# https://community.plotly.com/t/extend-or-append-data-instead-of-update/8898/7
# Drawing the layout ofthe dashboard (map, buttons, plot)
def run_dashboard(years_param, output_dir, vector_dir):
    global years, OUTPUT_DIR, VECTOR_DIR
    years = years_param
    OUTPUT_DIR = output_dir
    VECTOR_DIR = vector_dir

    app.layout = html.Div([
        html.H1("Mangrove expansion in Hainan", style={'paddingTop': '20px', 'textAlign': 'center'}),
        dl.Map(
            id="map",
            center=[19.2, 109.8],
            zoom=8,
            children=[
                dl.TileLayer(),
                dl.Rectangle(bounds=areas_of_interest["area1"]["bounds"], id="rect-area1"),
                dl.Rectangle(bounds=areas_of_interest["area2"]["bounds"], id="rect-area2"),
                dl.Rectangle(bounds=areas_of_interest["area3"]["bounds"], id="rect-area3"),
            ],
            style={'height': '60vh'},
        ),
        html.Div([
            html.Button("Area 1", id="btn-area1", n_clicks=0),
            html.Button("Area 2", id="btn-area2", n_clicks=0),
            html.Button("Area 3", id="btn-area3", n_clicks=0),
            html.Button("Reset view", id="btn-reset", n_clicks=0),
        ]),
        dcc.RadioItems(
            options=[
                {'label': 'NDVI', 'value': 'ndvi'},
                {'label': 'NDMI', 'value': 'ndmi'},
                {'label': 'Mangrove Extent', 'value': 'extent'},
            ],
            value='ndvi',
            id='layer-toggle'
        ),
        dcc.Slider(
            min(years), max(years), step=None, value=min(years),
            marks={str(year): str(year) for year in years},
            id='year-slider'
        ),
    ])

    app.run(debug=True)


# Source: https://dash.plotly.com/basic-callbacks
# Whenever the slider or the toggle changes, rebuild the map layers:
# base tiles, the three area rectangles, and the selected layer
@callback( # @callback makes dash interactive
    Output('map', 'children'),
    Input('year-slider', 'value'),
    Input('layer-toggle', 'value'))

def update_map(selected_year, layer_choice):
    # layers that always shown, regadless of the year or the toggle choice
    layers = [
        dl.TileLayer(),
        dl.Rectangle(bounds=areas_of_interest["area1"]["bounds"], id="rect-area1"),
        dl.Rectangle(bounds=areas_of_interest["area2"]["bounds"], id="rect-area2"),
        dl.Rectangle(bounds=areas_of_interest["area3"]["bounds"], id="rect-area3"),
    ]

    # Build the correct file path for the selected year, convert it to a PNG,
    # and add it as the one data layer matching the current toggle choice
    if layer_choice == "ndvi":
        raster_path = f"{OUTPUT_DIR}/NDVI_{selected_year}.tif"
        png_path = os.path.join("data", "assets", f"ndvi_{selected_year}.png")
        bounds = tif_to_png_singleband(raster_path, png_path, "RdYlGn", vmin=-0.2, vmax=0.8)
        layers.append(dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8))

    elif layer_choice == "ndmi":
        raster_path = f"{OUTPUT_DIR}/NDMI_{selected_year}.tif"
        png_path = os.path.join("data", "assets", f"ndmi_{selected_year}.png")
        bounds = tif_to_png_singleband(raster_path, png_path, "YlGnBu", vmin=-0.5, vmax=0.5)
        layers.append(dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8))

    # Source: https://leafletjs.com/examples/geojson/
    # Mangrove extent is vector data (shapefile), not a raster (there's no need to convert it)
    elif layer_choice == "extent":
        geojson = get_extent_geojson(selected_year)
        layers.append(dl.GeoJSON(data=geojson, id="extent-layer", style={"color": "green", "fillColor": "green", "weight": 2, "fillOpacity": 0.5}))
        

    # return all layers to this year/toggle
    return layers


# One callback per zoom button (each just flies the map to its own area)
# Soruce: https://dash.plotly.com/advanced-callbacks
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
    return dict(center=[19.2, 109.8], zoom=8, transition="flyTo")



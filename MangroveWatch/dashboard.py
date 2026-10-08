# Source: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
from dash import Dash, dcc, html, Input, Output, callback
import dash_leaflet as dl
import os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from PIL import Image

# Create a subfolder called assets inside data because dash needs it to store the png images
os.makedirs("data/assets", exist_ok=True)

# Source: https://nbviewer.org/format/script/github/jupyter-widgets/ipyleaflet/blob/0.16.0/examples/Numpy.ipynb
def tif_to_png_overlay(tif_path, png_path):
    """Convert GeoTIFFs into a PNGs + lat/lon bounds for dl.ImageOverlay."""
    with rasterio.open(tif_path) as src:
        arr = src.read([1, 2, 3])  # red, green, blue bands
        arr = np.clip(arr / np.nanpercentile(arr, 98) * 255, 0, 255).astype("uint8")
        arr = np.moveaxis(arr, 0, -1)
        Image.fromarray(arr).save(png_path)

        west, south, east, north = transform_bounds(src.crs, "EPSG:4326", *src.bounds)
        bounds = [[south, west], [north, east]]

    return bounds


# Map each year to its raster file path (placeholder names)
# Source: https://docs.python.org/3/library/functions.html#sorted
year_files = {
    1990: "data/image_1990.tif",
    1996: "data/image_1996.tif",
    2003: "data/image_2003.tif",
    2010: "data/image_2010.tif",
    2016: "data/image_2016.tif",
    2020: "data/image_2020.tif",
}
years = sorted(year_files.keys())

app = Dash()

# Sources: https://www.dash-leaflet.com/
# https://dash.plotly.com/component-argument-order
app.layout = html.Div([
    dl.Map(id="map", center=[19.2, 109.8], zoom=7, children=[
        dl.TileLayer(),
    ], style={'height': '60vh'}),

    dcc.Slider(
        min(years),
        max(years),
        step=None,
        value=min(years),
        marks={str(year): str(year) for year in years},
        id='year-slider'
    )
])


@callback(
    Output('map', 'children'),
    Input('year-slider', 'value'))
def update_map(selected_year):
    raster_path = year_files[selected_year]
    png_path = os.path.join("data", "assets", os.path.basename(raster_path).replace(".tif", ".png"))
    bounds = tif_to_png_overlay(raster_path, png_path)

    return [
        dl.TileLayer(),
        dl.ImageOverlay(url=f"/assets/{os.path.basename(png_path)}", bounds=bounds, opacity=0.8),
    ]


if __name__ == '__main__':
    app.run(debug=True)
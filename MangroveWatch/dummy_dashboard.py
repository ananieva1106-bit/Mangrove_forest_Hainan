# Sources: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
# https://nbviewer.org/format/script/github/jupyter-widgets/ipyleaflet/blob/0.16.0/examples/Numpy.ipynb
# https://www.dash-leaflet.com/
# https://dash.plotly.com/component-argument-order
from dash import Dash, dcc, html, Input, Output, callback
import dash_leaflet as dl

app = Dash()

# Dummy areas of interest
areas_of_interest = {
    "area1": {"label": "Area 1", "center": [19.85, 109.45], "zoom": 13},
    "area2": {"label": "Area 2", "center": [19.55, 110.45], "zoom": 13},
    "area3": {"label": "Area 3", "center": [18.65, 109.65], "zoom": 13},
}

years = [1990, 1996, 2003, 2010, 2016, 2020]

app.layout = html.Div([
    dl.Map(
        id="map",
        center=[19.2, 109.8],
        zoom=7,
        children=[
            dl.TileLayer(),
            # Dummy rectangles marking the three areas of interest
            dl.Rectangle(bounds=[[19.80, 109.40], [19.90, 109.50]], id="rect-area1"),
            dl.Rectangle(bounds=[[19.50, 110.40], [19.60, 110.50]], id="rect-area2"),
            dl.Rectangle(bounds=[[18.60, 109.60], [18.70, 109.70]], id="rect-area3"),
        ],
        style={'height': '60vh'},
    ),

    html.Div([
        html.Button("Zoom to Area 1", id="btn-area1", n_clicks=0),
        html.Button("Zoom to Area 2", id="btn-area2", n_clicks=0),
        html.Button("Zoom to Area 3", id="btn-area3", n_clicks=0),
        html.Button("Reset view", id="btn-reset", n_clicks=0),
    ]),

    dcc.Slider(
        min(years), max(years), step=None, value=min(years),
        marks={str(year): str(year) for year in years},
        id='year-slider'
    ),

    html.Div(id="status-text"),
])


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
    from dash import ctx
    triggered = ctx.triggered_id

    if triggered == "btn-area1":
        a = areas_of_interest["area1"]
        return dict(center=a["center"], zoom=a["zoom"], transition="flyTo")
    elif triggered == "btn-area2":
        a = areas_of_interest["area2"]
        return dict(center=a["center"], zoom=a["zoom"], transition="flyTo")
    elif triggered == "btn-area3":
        a = areas_of_interest["area3"]
        return dict(center=a["center"], zoom=a["zoom"], transition="flyTo")
    else:  # reset
        return dict(center=[19.2, 109.8], zoom=7, transition="flyTo")


# Status text -
@callback(
    Output("status-text", "children"),
    Input("year-slider", "value"))
def update_status(selected_year):
    return f"Showing data for: {selected_year}"


if __name__ == '__main__':
    app.run(debug=True)
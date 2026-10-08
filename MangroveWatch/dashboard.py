# Source: https://dash.plotly.com/basic-callbacks#dash-app-layout-with-figure-and-slider
from dash import Dash, dcc, html, Input, Output, callback
import dash_leaflet as dl

app = Dash()

app.layout = html.Div([
    dl.Map(id="map", center=[19.2, 109.8], zoom=8,
           children=[dl.TileLayer()],
           style={'height': '60vh'}),

    dcc.Slider(1990, 2020, step=None, value=1990,
               marks={1990: '1990', 1996: '1996', 2016: '2016', 2020: '2020'},
               id='year-slider'),
])

@callback(
    Output('map', 'children'),
    Input('year-slider', 'value'))
def update_map(selected_year):
    print(f"Slider moved to: {selected_year}")  # just prove the callback fires
    return [dl.TileLayer()]  # placeholder -- same thing every time, for now

if __name__ == '__main__':
    app.run(debug=True)



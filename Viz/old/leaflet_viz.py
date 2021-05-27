import pandas as pd
import numpy as np
from datetime import datetime, date

import plotly.express as px
import plotly.graph_objects as go

import folium
from folium.plugins import HeatMap
import altair as alt

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.dependencies import Input, Output


data = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/pred_data.csv")
data["transdate"] = pd.to_datetime(data["transdate"])
data["hour"] = data["transdate"].dt.hour

bus_route = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/bus_route.csv")

# bus_no_dict
unq_bus_no = np.sort(data["bus_no"].unique())
bus_no_dict = [{"label" : x, "value" : x} for x in unq_bus_no]


temp_data = data.loc[data["transdate"] == pd.to_datetime("2020-04-08 05:00:00")].copy()

f = folium.Figure(width=1600, height=1000)
m = folium.Map([35.539302, 129.338169], zoom_start=13, width=1600, height=1000)


temp_data2 = data.loc[(data["transdate"].dt.date == date.fromisoformat("2020-04-08")) & (data["stop_id"] == 40403)]
chart = alt.Chart(temp_data2).mark_line().encode(
    x = "hour",
    y = "totalcnt"
)

line = alt.Chart(pd.DataFrame({'hour': [12]})).mark_rule(color="red").encode(x='hour')

chart = chart + line



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
button = dbc.Card(
    dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        html.H5("Bus No."),
                        dcc.Dropdown(
                            id = "bus_no_dropdown",
                            options = bus_no_dict,
                            value = "401"
                        )
                    ]
                ),
                width = {"size": 2}
            ),

            dbc.Col(
                dbc.FormGroup(
                    [
                        html.H5("Bus Route"),
                        dcc.Dropdown(
                            id = "bus_route_dropdown",
                        )
                    ]
                ),
                width = {"size": 2}
            ),

            dbc.Col(
                dbc.FormGroup(
                    [
                        html.H5("Select Date"),
                        dcc.DatePickerSingle(
                            id = "date_picker_single",
                            min_date_allowed = data["transdate"].dt.date.min(),
                            max_date_allowed = data["transdate"].dt.date.max(),
                            initial_visible_month = data["transdate"].dt.date.min(),
                            date = data["transdate"].dt.date.min()
                        )
                    ],
                    row = False
                ),
                width = {"size": 1}
            ),

            dbc.Col(
                dbc.FormGroup(
                    [
                        html.H5("Select Hour"),
                        dcc.Slider(
                            id = "time_slider",
                            min = 0,
                            max = 23,
                            step = 1,
                            value = 12,
                            marks = {i : f"{i}" for i in range(24)}
                        )
                    ]
                ),
                width = {"size": 7}
            )

        ],
        align = "start"
    ),
    body = True
)

geojson = dl.GeoJSON(data)

app.layout = dbc.Container(
    [
        dbc.Row(html.H1("울산광역시 시내 버스 수요 예측"), justify="center"),
        dbc.Row(
            [
                dbc.Col(button, width = 8)
                # dbc.Col(bus_no_dropdown, width = 1),
                # dbc.Col(bus_route_dropdown, width = 1),
                # dbc.Col(date_picker_single, width = 1),
                # dbc.Col(time_slider, width = 3),
            ],
            justify = "center"
        ),
        dbc.Row(
            dbc.Col(
                dl.Map(dl.TileLayer(),  zoom=10, id = "scatter"),

                width = 8
            ),
            style={"height" : "1000vh"},
            justify = "center"
        )
    ],
    fluid = True
)

#################################################################################################################################







    
# folium.Popup(folium.Html('aa<br>'+folium.IFrame(temp_html, width='410px', height='410px').render(), script=True), max_width=2650)
if __name__ == "__main__":
    # app.run_server(debug = True, port = 8899, host="127.0.0.0")
    app.run_server(debug = True)
    
import pandas as pd
import numpy as np
from datetime import datetime, date
from collections import defaultdict

import plotly.express as px
import plotly.graph_objects as go

import folium
from folium.plugins import HeatMap
import altair as alt

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import branca.colormap

## 1. Data Load ## 

# Bus Data
data = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/pred_data.csv")
data["transdate"] = pd.to_datetime(data["transdate"])
data["hour"] = data["transdate"].dt.hour

# Bus Route Data
bus_route = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/bus_route.csv")

# bus_no_dict
unq_bus_no = np.sort(data["bus_no"].unique())
bus_no_dict = [{"label" : x, "value" : x} for x in unq_bus_no]




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

## 2. Layout ##

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
                            value = "All"
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
                        html.H5("Select Hour", style = {"padding-left" : "20px"}),
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

app.layout = dbc.Container(
    [
        dbc.Row(html.H1("울산광역시 시내 버스 수요 예측"), justify="center"),
        dbc.Row(
            [
                dbc.Col(button, width = 8)
            ],
            justify = "center"
        ),
        dbc.Row(
            dbc.Col(
                html.Iframe(
                    id = "scatter",
                    width = "100%",
                    height = "100%",

                ),
                width = 8
            ),
            style={"height" : "70vh"},
            justify = "center"
        )
    ],
    fluid = True
)

#################################################################################################################################

# line plot for popup (daily trend)
def draw_line_plot(data, date, hour, stop_id):
    temp_data = data.loc[(data["transdate"].dt.date == date) & (data["stop_id"] == stop_id)]

    chart = alt.Chart(temp_data, title=f"{temp_data['stop_nm'].unique()[0]} ({stop_id})").mark_line().encode(
        x = "hour",
        y = "totalcnt"
    )

    line = alt.Chart(pd.DataFrame({'hour': [hour]})).mark_rule(color="red").encode(x='hour')

    return chart + line

# Callback Function
@app.callback(
    dash.dependencies.Output("bus_route_dropdown", "options"),
    dash.dependencies.Input("bus_no_dropdown", "value")
)
def update_bus_route_menu(bus_no):
    unq_bus_route = data.loc[data["bus_no"] == bus_no, "route"].unique()

    bus_route_dict = [{"label" : "All", "value" : "All"}]
    for x in unq_bus_route:
        bus_route_dict.append({"label" : x, "value" : x})

    return bus_route_dict



@app.callback(
    dash.dependencies.Output("scatter", "srcDoc"),

    dash.dependencies.Input("date_picker_single", "date"),
    dash.dependencies.Input("time_slider", "value"),
    dash.dependencies.Input("bus_no_dropdown", "value"),
    dash.dependencies.Input("bus_route_dropdown", "value")
)
def draw_folium_map(date_value, time_value, bus_no="401", route="All"):

    date_object = date.fromisoformat(date_value)

    # bus data
    if route == "All":
        daily_data = data.loc[(data["transdate"].dt.date == date_object) & (data["bus_no"] == bus_no)]
    else:
        daily_data = data.loc[(data["transdate"].dt.date == date_object) & (data["bus_no"] == bus_no) & (data["route"] == route)]

    hourly_data = daily_data.loc[(daily_data["transdate"].dt.hour == int(time_value))]
    
    # bus route data
    bus_route = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/bus_route.csv")
    if route == "All":
        bus_route = bus_route.loc[(bus_route["bus_no"] == bus_no)]
    else:
        bus_route = bus_route.loc[(bus_route["bus_no"] == bus_no) & (bus_route["route"] == route)]
    


    m = folium.Map([35.539302, 129.338169], zoom_start=13)

    heat_map = folium.FeatureGroup("HeatMap")
    bus_line = folium.FeatureGroup("BusLine")
    bus_stop = folium.FeatureGroup("BusStop")


    # Heatmap
    HeatMap(hourly_data[['latitude','longitude', "totalcnt"]], opacity = 0.5).add_to(heat_map)

    # Bus Line
    for j, rt in enumerate(bus_route["route"].unique()):
        temp_route = bus_route.loc[bus_route["route"] == rt]
        coord_list = temp_route[["latitude", "longitude"]].values
        
        folium.PolyLine(coord_list, color = ["red", "blue"][j], opacity = 0.5, tooltip = f"<b>노선</b> : {rt}").add_to(bus_line)


    # Bus Stop
    for i, row in hourly_data.iterrows():
        popup = folium.map.Popup(f"""정류장 명 : {row['stop_nm']} <br> 탑승자 수 : {row['totalcnt']}""",
                                 max_width = "1000")
        
        # draw line chart
        line_chart = draw_line_plot(data = daily_data, date = date_object, hour = int(time_value), stop_id=row["stop_id"])


        folium.CircleMarker(
            location = [row["latitude"], row["longitude"]],
            radius = 5,
            popup = folium.map.Popup().add_child(folium.VegaLite(line_chart, width='100%', height='100%')),
            tooltip= f"""<b>정류장 ID</b>: {row['stop_id']}<br>
                         <b>정류장 명</b>: {row['stop_nm']}<br>
                         <b>노선</b>: {row['bus_no']}({row['route']})<br>
                         <b>예상 탑승자 수</b>: {row['totalcnt']}""",
            color = "#3186cc",
            fill = True,
            fill_color = "#3186cc",
            fill_opacity=1
        ).add_to(bus_stop)

    heat_map.add_to(m)
    bus_line.add_to(m)
    bus_stop.add_to(m)


    folium.LayerControl().add_to(m)
    
    m.save("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html")
    return open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html", "r").read()



if __name__ == "__main__":
    app.run_server(debug = True)
    
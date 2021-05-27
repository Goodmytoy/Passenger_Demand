import pandas as pd
import numpy as np
from datetime import datetime, date

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


data = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/base_data.csv")
data["transdate"] = pd.to_datetime(data["transdate"])

temp_data = data.loc[data["transdate"] == pd.to_datetime("2020-04-08 05:00:00")].copy()

fig = px.scatter_mapbox(temp_data, 
                        lat=temp_data["latitude"], 
                        lon=temp_data["longitude"], 
                        color ="totalcnt",
                        size = "totalcnt",
                        hover_name= "stop_nm", 
                        # hover_template="",
                        hover_data= {"latitude" : False,
                                     "longitude" : False},
                        color_discrete_sequence=["fuchsia"], 
                        zoom=12, 
                        height=1000)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



app = dash.Dash(__name__)
app.layout = html.Div(children = [
    html.H1("울산광역시 시내 버스 수요 예측 (2020.04 ~ 2020.12)"),
    html.Div(children = [dcc.DatePickerSingle(
                             id = "date_picker_single",
                             min_date_allowed = data["transdate"].dt.date.min(),
                             max_date_allowed = data["transdate"].dt.date.max(),
                             initial_visible_month = data["transdate"].dt.date.min(),
                             date = data["transdate"].dt.date.min()),
                         dcc.Slider(id = "time_slider", 
                                    min = 0,
                                    max = 23,
                                    step = 1,
                                    value = 12,
                                    marks = {i : f"{i}시" for i in range(24)})
                        ],
                        style = {"display" : "grid", "grid-template-columns": "8% 50%"}),

    # html.Iframe(
    #     id = "scatter", 
    #     # srcDoc = open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html", "r").read(),
    #     width = "1600", height = "1000"),
    html.Div(children = dcc.Graph(
                             id="scatter",
                             figure = fig
                         ),
             style = {"width" : "60%"}
            )
])

# @app.callback(
#     dash.dependencies.Output("scatter", "srcDoc"),
#     dash.dependencies.Input("date_picker_single", "date"),
#     dash.dependencies.Input("time_slider", "value")
# )
# def draw_circle(date_value, time_value):
#     f = folium.Figure(width=1600, height=1000)
#     m = folium.Map([35.539302, 129.338169], zoom_start=13, width=1600, height=1000)
#     date_object = date.fromisoformat(date_value)
#     temp_data = data.loc[(data["transdate"].dt.date == date_object) & (data["transdate"].dt.hour == int(time_value))]
#     for i, row in temp_data.iterrows():
#         popup = folium.map.Popup(f"""정류장 명 : {row['stop_nm']} <br> 탑승자 수 : {row['totalcnt']}""",
#                                 #  parse_html = True,
#                                  max_width = "1000")
#         folium.CircleMarker(
#             location = [row["latitude"], row["longitude"]],
#             radius = 5,
#             popup = popup,
#             tooltip= f"<b>정류장 명</b>: {row['stop_nm']}<br><b>탑승자 수</b>: {row['totalcnt']}",
#             color = "#3186cc",
#             fill = True,
#             fill_color = "#3186cc",
#             fill_opacity=1
#         ).add_to(m)
    
#     m.save("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html")
#     return open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html", "r").read()

if __name__ == "__main__":
    # app.run_server(debug = True, port = 8899, host="127.0.0.0")
    app.run_server(debug = True)
    
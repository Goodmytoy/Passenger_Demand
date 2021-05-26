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
from dash.dependencies import Input, Output


data = pd.read_csv("/home/seho/all-spark-notebook/Passenger_Demand/data/base_data.csv")
data["transdate"] = pd.to_datetime(data["transdate"])
data["hour"] = data["transdate"].dt.hour

# bus_no_dict
unq_bus_no = np.sort(data["bus_no"].unique())
bus_no_dict = [{"label" : x, "value" : x} for x in unq_bus_no]
# print(bus_no_dict)


temp_data = data.loc[data["transdate"] == pd.to_datetime("2020-04-08 05:00:00")].copy()
# temp_data["hour"] = temp_data["transdate"].dt.hour

f = folium.Figure(width=1600, height=1000)
m = folium.Map([35.539302, 129.338169], zoom_start=13, width=1600, height=700)


# plotly
temp_data2 = data.loc[(data["transdate"].dt.date == date.fromisoformat("2020-04-08")) & (data["stop_id"] == 40403)]
# fig = px.line(temp_data2, x="hour", y="totalcnt", title = "하루 탑승자 추세")

chart = alt.Chart(temp_data2).mark_line().encode(
    x = "hour",
    y = "totalcnt"
)

line = alt.Chart(pd.DataFrame({'hour': [12]})).mark_rule(color="red").encode(x='hour')

chart = chart + line



app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children = [
    html.H1("울산광역시 시내 버스 수요 예측 (2020.04 ~ 2020.12)"),
    html.Div(children = [dcc.Dropdown(
                             id = "bus_no_dropdown",
                             options = bus_no_dict,
                             value = "401"),
                             
                         html.Div(),
                         dcc.DatePickerSingle(
                             id = "date_picker_single",
                             min_date_allowed = data["transdate"].dt.date.min(),
                             max_date_allowed = data["transdate"].dt.date.max(),
                             initial_visible_month = data["transdate"].dt.date.min(),
                             date = data["transdate"].dt.date.min(),
                             style = {"margin-bottom" : "100"}),

                         dcc.Slider(id = "time_slider", 
                                    min = 0,
                                    max = 23,
                                    step = 1,
                                    value = 12,
                                    marks = {i : f"{i}시" for i in range(24)})
                        ],
                        style = {"display" : "grid", "grid-template-columns": "5% 1% 8% 50%"},
                        ),

    html.Div(
        html.Iframe(
            id = "scatter", 
            width = "1600", 
            height = "1000"),
        style = {"height" : "200%"}
    ),

])


def draw_line_plot(data, date, hour, stop_id):
    temp_data = data.loc[(data["transdate"].dt.date == date) & (data["stop_id"] == stop_id)]

    chart = alt.Chart(temp_data).mark_line().encode(
        x = "hour",
        y = "totalcnt"
    )

    line = alt.Chart(pd.DataFrame({'hour': [hour]})).mark_rule(color="red").encode(x='hour')

    return chart + line


# Callback Function
@app.callback(
    dash.dependencies.Output("scatter", "srcDoc"),
    dash.dependencies.Input("date_picker_single", "date"),
    dash.dependencies.Input("time_slider", "value")
)
def draw_folium_map(date_value, time_value):
    f = folium.Figure(width=1600, height=1000)
    m = folium.Map([35.539302, 129.338169], zoom_start=13, width=1600, height=1000)
    date_object = date.fromisoformat(date_value)
    hourly_data = data.loc[(data["transdate"].dt.date == date_object) & (data["transdate"].dt.hour == int(time_value))]
    daily_data = data.loc[(data["transdate"].dt.date == date_object)]
    
    # for id in temp_data["stop_id"].unique():
    #     open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/daily_line_plot/id.html", "r").read()
    temp_html = open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/temp.html", "r").read()
    # print(temp_html)
    for i, row in hourly_data.iterrows():
        popup = folium.map.Popup(f"""정류장 명 : {row['stop_nm']} <br> 탑승자 수 : {row['totalcnt']}""",
                                #  parse_html = True,
                                 max_width = "1000")
        
        # draw line chart
        # line_chart = draw_line_plot(data = daily_data, date = date_object, hour = int(time_value), stop_id=row["stop_id"])


        folium.CircleMarker(
            location = [row["latitude"], row["longitude"]],
            radius = 5,
            # popup = folium.Popup(folium.Html(folium.IFrame(temp_html, width='410px', height='410px').render](), script=True), max_width=2650),
            popup = folium.map.Popup().add_child(folium.VegaLite(chart, width='100%', height='100%')),
            tooltip= f"<b>정류장 명</b>: {row['stop_nm']}<br><b>탑승자 수</b>: {row['totalcnt']}",
            color = "#3186cc",
            fill = True,
            fill_color = "#3186cc",
            fill_opacity=1
        ).add_to(m)
    
    m.save("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html")
    return open("/home/seho/all-spark-notebook/Passenger_Demand/Viz/scatter.html", "r").read()





    
# folium.Popup(folium.Html('aa<br>'+folium.IFrame(temp_html, width='410px', height='410px').render(), script=True), max_width=2650)
if __name__ == "__main__":
    # app.run_server(debug = True, port = 8899, host="127.0.0.0")
    app.run_server(debug = True)
    
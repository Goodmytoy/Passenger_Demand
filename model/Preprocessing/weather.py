import pandas as pd
import numpy as np

def preprocess_weather_data(weather_data):
    """
        날씨 데이터를 전처리 하는 함수
        
        Args: 
            weather_data: 날씨 데이터 (Pandas.DataFrame)

        Returns: 
            data: 날씨 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """     
    # 필요 컬럼만 추출
    # tm(시간), ta(기온), hm(습도), rn(강수량), dsnw(적설량)
    weather_data = weather_data.loc[:, ["tm", "ta", "hm", "rn", "dsnw"]]
    weather_data = weather_data.rename(columns = {"tm" : "time",
                                                  "ta" : "temperature",
                                                  "hm" : "humidity",
                                                  "rn" : "precipitation",
                                                  "dsnw" : "snowfall",})
    weather_data["time"] = pd.to_datetime(weather_data["time"], format = "%Y-%m-%d %H:%M")
    
    for col in ["temperature", "humidity", "precipitation", "snowfall"]:
        weather_data[col] = weather_data[col].replace("", "0.0").astype(float)
        weather_data[col] = weather_data[col].astype(float)
        
    weather_data["time_hours"] = weather_data["time"].dt.strftime("%Y-%m-%d %H")
    weather_data = weather_data.drop("time", 1)
    
    return weather_data
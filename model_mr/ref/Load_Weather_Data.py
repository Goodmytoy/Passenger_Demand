from utils.Weather_Data_by_API import *
import os

def Load_Weather_Data(params_dict,
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    weather_api = Weather_Data_by_API(params_dict = params_dict)
    weather_data = weather_api.get()
    
    
    # index 초기화
    weather_data = weather_data.drop_duplicates().reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        weather_data.to_csv(save_path +'/weather_data.csv', index=False)
    else :
        return weather_data
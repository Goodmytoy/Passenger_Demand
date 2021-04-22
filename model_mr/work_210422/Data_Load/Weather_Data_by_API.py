import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *



class Weather_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?"
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["dataType"].lower()
    
    
    def get(self):
        
        self.request_urls = self.create_request_urls()

        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
            text_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in text_dict.items():
                data_dict[k].extend(v)
            
        return pd.DataFrame(data_dict)
    
    
def Load_Weather_Data(params_dict,
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    weather_api = Weather_Data_by_API(params_dict = params_dict)
    weather_data = weather_api.get()
    
    
    # index 초기화
    weather_data = weather_data.drop_duplicates().reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        weather_data.to_csv(save_path +'/weather_data.csv', index=False)
    else :
        return weather_data
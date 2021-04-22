import pandas as pd
import numpy as np
import os 
from collections import defaultdict
from .Data_by_API import *

class Holiday_Data_by_API(Data_by_API):
    
    holiday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo?"
    restday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?"
    
    def __init__(self, params_dict, type):
        if type == "holi":
            base_url = self.holiday_url
        elif type == "rest":
            base_url = self.restday_url
            
        super().__init__(url = base_url)
#         self.year = year
        self.params_dict = params_dict
        self.type = "xml"
        
    
    def create_request_urls(self, params_dict):
        params_dict = params_dict.copy()
        request_urls = []
        for x in range(1, 13):
            if x < 10:
                params_dict["solMonth"] =  f"0{str(x)}"

            else:
                params_dict["solMonth"] =  str(x)
                
            request_urls.append(self.create_request_url(params_dict = params_dict))
    
        return request_urls
    
    
    def get(self):
        
        if "solMonth" in self.params_dict.keys():
            self.request_urls = [self.create_request_url(params_dict = self.params_dict)]
        else:             
            self.request_urls = self.create_request_urls(params_dict = self.params_dict)
        
        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            
            rq = super().request(request_url = request_url)
            temp_dict = super().parse(request = rq, features = ["locdate", "dateName"], type = self.type)
            
            for k, v in temp_dict.items():
                data_dict[k].extend(v)

                    
        return pd.DataFrame(data_dict)
    


def Load_Holiday_Data(params_dict,
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    holiday_api = Holiday_Data_by_API(params_dict = params_dict, type = "rest")
    holiday_data = holiday_api.get()
    
    # index 초기화
    holiday_data = holiday_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        holiday_data.to_csv(save_path +'/holiday_data.csv', index=False)
    else :
        return holiday_data
    
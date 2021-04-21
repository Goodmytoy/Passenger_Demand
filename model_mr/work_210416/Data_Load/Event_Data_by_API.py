import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class Event_Data_by_API(Data_by_API):
    
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_pblprfr_event_info_api?" # XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("type")
    
    def create_request_urls(self):
        max_page = self.calculate_max_page(type = self.type)
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["pageNo"] = i + 1
            request_urls.append(super().create_request_url(params_dict = params_dict))
            
        return request_urls
  
    
    def get(self):
        
        self.request_urls = self.create_request_urls()
        
        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
            temp_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
            
        return pd.DataFrame(data_dict)

    
    
    
def Load_Event_Data(params_dict,
                    start_year = '',
                    end_year = '',
                    select_region = '', 
                    save_tf = False, 
                    save_path = os.getcwd()):
    
    event_api = Event_Data_by_API(params_dict = params_dict)
    event_data = event_api.get()
    
    # 날짜데이터 형변환
    event_data["eventStartDate"] = pd.to_datetime(event_data["eventStartDate"], format = "%Y-%m-%d")
    event_data["eventEndDate"] = pd.to_datetime(event_data["eventEndDate"], format = "%Y-%m-%d")
    event_data["referenceDate"] = pd.to_datetime(event_data["referenceDate"], format = "%Y-%m-%d")

    # 선택된 지역 데이터 추출
    if select_region != '':
        event_data = event_data.loc[event_data["rdnmadr"].str.contains(select_region)]
        
    # 시작연도 데이터 추출
    if start_year != '':
        event_data = event_data.loc[(event_data["eventStartDate"].dt.year.between(start_year, end_year))]
    
    # index 초기화
    event_data = event_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        event_data.to_csv(save_path +'/event_data.csv', index=False)
    else :
        return event_data

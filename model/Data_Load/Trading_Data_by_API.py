  
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *
from .Geocoding_by_API import *


class Trading_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/B553077/api/open/sdsc/storeOne?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        params_dict['cx'] = gmaps.geocode(params_dict.get('region'))[0]["geometry"]["location"]['lat']
        params_dict['cy'] = gmaps.geocode(params_dict.get('region'))[0]["geometry"]["location"]['lng']
        self.cx = params_dict.get('cx')
        self.cy = params_dict.get('cy')
        
        del params_dict['region']
        
        self.params_dict = params_dict  
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.type = params_dict.get("type")
        
    def create_request_url(self, params_dict):
#         params_dict["service_key"] = self.serviceKey
        params_list = [f"{k}={v}" for k, v in params_dict.items()]
        params_str = "&".join(params_list)
#         print(params_str)
        
        self.request_url = self.url + params_str
        print(self.request_url)
        return self.request_url
    
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
    
    


def Load_Trading_Data(params_dict,
                      google_key,
                      select_region = '', 
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    trading_api = Trading_Data_by_API(params_dict = params_dict)
    trading_data = trading_api.get()
    
    # 날짜데이터 형변환
    trading_data["updateDt"] = pd.to_datetime(trading_data["updateDt"], format = "%Y-%m-%d")
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        trading_data = trading_data.loc[trading_data["siteWhlAddr"].str.contains(select_region)]
    
    # Geocoding
    trading_data = get_geocodeDf(trading_data, "rdnWhlAddr", google_key)
    
    # index 초기화
    trading_data = trading_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        trading_data.to_csv(save_path +'/trading_data.csv', index=False)
    else :
        return university_data    
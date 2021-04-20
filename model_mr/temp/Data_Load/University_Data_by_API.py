# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *
from .Geocoding_by_API import *

class University_Data_by_API(Data_by_API):
    
    base_url = "http://www.career.go.kr/cnet/openapi/getOpenApi?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("contentType")
    
    
    def extract_values_from_dict(self, dct):
        try: 
            dict_list = dct["dataSearch"]["content"]
        except:
            dict_list = dct["dataSearch"]["content"]
        
        return dict_list
    
    
    def create_request_urls(self):
        max_page = 1
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["thisPage"] = i + 1
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



def Load_University_Data(params_dict,
                         google_key,
                         select_region = '', 
                         save_tf = False, 
                         save_path = os.getcwd()):
    
    university_api = University_Data_by_API(params_dict = params_dict)
    university_data = university_api.get()
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        university_data = university_data.loc[university_data["region"].str.contains(select_region)]

    # Geocoding
    university_data = get_geocodeDf(university_data, "adres", google_key)
    
    # index 초기화
    university_data = university_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        university_data.to_csv(save_path +'/university_data.csv', index=False)
    else :
        return university_data

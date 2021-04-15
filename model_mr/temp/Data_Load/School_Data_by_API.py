# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class School_Data_by_API(Data_by_API):
    
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_elesch_mskul_lc_api?"
    
    def __init__(self, params_dict):
        """
            School_Data_by_API Class의 생성자

            Args: 
                params_dict : API Request Parameters (Dictionary)
                
            Returns:
                
            Exception: 
        """
        
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["type"]
  
    
    def get(self):
        """
            API로 데이터를 받아서 Pandas DataFrame 형태로 반환하는 Method

            Args: 
                
            Returns:
                (Pandas DataFrame)
                
            Exception: 
        """
        
        self.request_urls = self.create_request_urls()
        
        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
#             temp_dict = self.parse_json(request = rq, features = None)
            temp_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
        
    
        return pd.DataFrame(data_dict)



def Load_School_Data(params_dict,
                     select_region = '',
                     save_tf = False, 
                     save_path = os.getcwd()):
    
    school_api = School_Data_by_API(params_dict = params_dict)
    school_data = school_api.get()
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        school_data = school_data.loc[school_data["rdnmadr"].str.contains(select_region)]
        
    # index 초기화
    school_data = school_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        school_data.to_csv(save_path +'/school_data.csv', index=False)
    else :
        return school_data


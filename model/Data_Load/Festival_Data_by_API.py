import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class Festival_Data_by_API(Data_by_API):
    """
        API를 통해 축제 데이터를 가져오는 Class
    """
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("type")
  
    
    
def Load_Festival_Data(params_dict, 
                       start_year = '',
                       end_year = '',
                       select_region = '', 
                       save_tf = False, 
                       save_path = os.getcwd()):
    """
        축제 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            start_year: 데이터 시작 년도 (str)
            end_year: 데이터 종료 년도 (str)
            select_region: 지역명 (str)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            festival_data: 축제 데이터 (Pandas.DataFrame)

        Exception: 
    """
    festival_api = Festival_Data_by_API(params_dict = params_dict)
    festival_data = festival_api.get()
    
    # 날짜데이터 형변환
    festival_data["fstvlStartDate"] = pd.to_datetime(festival_data["fstvlStartDate"], format = "%Y-%m-%d")
    festival_data["fstvlEndDate"] = pd.to_datetime(festival_data["fstvlEndDate"], format = "%Y-%m-%d")
    festival_data["referenceDate"] = pd.to_datetime(festival_data["referenceDate"], format = "%Y-%m-%d")

    # 선택된 지역 데이터 추출
    if select_region != '':
        festival_data = festival_data.loc[festival_data["rdnmadr"].str.contains(select_region)]
        
    # 시작연도 데이터 추출
    if start_year != '':
        festival_data = festival_data.loc[(festival_data["fstvlStartDate"].dt.year.between(int(start_year), int(end_year)))]
    
    # index 초기화
    festival_data = festival_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        festival_data.to_csv(save_path +'/festival_data.csv', index=False)
    else :
        return festival_data
    
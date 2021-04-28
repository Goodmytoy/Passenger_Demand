import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class Event_Data_by_API(Data_by_API):
    """
        API를 통해 행사 데이터를 가져오는 Class
    """
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_pblprfr_event_info_api?" # XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("type")

    
    
def Load_Event_Data(params_dict,
                    start_year = '',
                    end_year = '',
                    select_region = '', 
                    save_tf = False, 
                    save_path = os.getcwd()):
    """
        행사 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            start_year: 데이터 시작 년도 (str)
            end_year: 데이터 종료 년도 (str)
            select_region: 지역명 (str)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            event_data: 행사 데이터 (Pandas.DataFrame)

        Exception: 
    """
    
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
        event_data = event_data.loc[(event_data["eventStartDate"].dt.year.between(int(start_year), int(end_year)))]
    
    # index 초기화
    event_data = event_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        event_data.to_csv(save_path +'/event_data.csv', index=False)
    else :
        return event_data

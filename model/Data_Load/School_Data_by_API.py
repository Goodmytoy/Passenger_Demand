import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class School_Data_by_API(Data_by_API):
    """
        API를 통해 학교(초중고) 데이터를 가져오는 Class
    """
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_elesch_mskul_lc_api?"
    
    def __init__(self, params_dict):
        """
            School_Data_by_API Class의 생성자

            Args: 
                params_dict : API 요청 파라미터 (Dictionary)

            Returns:
                
            Exception: 
        """
        
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["type"]
  


def Load_School_Data(params_dict,
                     select_region = '',
                     save_tf = False, 
                     save_path = os.getcwd()):
    """
        학교(초중고) 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            select_region: 지역명 (str)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            school_data: 학교(초중고) 데이터 (Pandas.DataFrame)

        Exception: 
    """
    school_api = School_Data_by_API(params_dict = params_dict)
    school_data = school_api.get()
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        school_data = school_data.loc[school_data["rdnmadr"].str.contains(select_region)]
        
    # index 초기화
    school_data = school_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        school_data.to_csv(save_path +'/school_data.csv', index=False)
    else :
        return school_data
    
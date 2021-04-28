import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class PM_Data_by_API(Data_by_API):
    """
        API를 통해 미세먼지 경보 데이터를 가져오는 Class
    """

    base_url = "http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo?"
    
    def __init__(self, params_dict):
        """
            PM_Data_by_API Class의 생성자

            Args: 
                params_dict : API 요청 파라미터 (Dictionary)
                
            Returns:
                
            Exception: 
        """
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["returnType"]
    
    

def Load_Particulate_Matter_Data(params_dict,
                                 save_tf = False, 
                                 save_path = os.getcwd()):
    """
        미세먼지 경보 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            pm_data: 미세먼지 경보 데이터 (Pandas.DataFrame)

        Exception: 
    """
    pm_api = PM_Data_by_API(params_dict = params_dict)
    pm_data = pm_api.get()
    
    # index 초기화
    pm_data = pm_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        pm_data.to_csv(save_path +'/pm_data.csv', index=False)
    else :
        return pm_data
    
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class Hospital_Data_by_API(Data_by_API):
    """
        API를 통해 병원 데이터를 가져오는 Class
    """
    
    base_url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?"
    
    def __init__(self, params_dict):
        """
            Hospital_Data_by_API Class의 생성자

            Args: 
                params_dict : params_dict: API 요청 파라미터 (Dictionary)
                
            Returns:
                
            Exception: 
        """
        
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = "xml"
  
    
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
        features = ['addr', 'clCd', 'clCdNm', 'drTotCnt', 'estbDd', 'gdrCnt', 'hospUrl', 'intnCnt', 'postNo', 'resdntCnt', 'sdrCnt', 'sgguCd', 'sgguCdNm', 'sidoCd', 'sidoCdNm', 'telno', 'XPos', 'YPos', 'yadmNm', 'ykiho']
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
            temp_dict = self.parse(request = rq, features = features, type = self.type)
            self.temp_dict = temp_dict       
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
        
        self.data_dict = data_dict
        return pd.DataFrame(data_dict)
    


def Load_Hospital_Data(params_dict,
                       save_tf = False, 
                       save_path = os.getcwd()):
    """
        병원 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            hospital_data: 병원 데이터 (Pandas.DataFrame)

        Exception: 
    """
    hospital_api = Hospital_Data_by_API(params_dict = params_dict)
    hospital_data = hospital_api.get()
    
    
    # index 초기화
    hospital_data = hospital_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        hospital_data.to_csv(save_path +'/hospital_data.csv', index=False)
    else :
        return hospital_data
    
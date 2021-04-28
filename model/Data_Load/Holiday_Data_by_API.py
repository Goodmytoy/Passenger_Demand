import pandas as pd
import numpy as np
import os 
from collections import defaultdict
from .Data_by_API import *

class Holiday_Data_by_API(Data_by_API):
    """
        API를 통해 휴일 데이터를 가져오는 Class
    """    
    # holiday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo?"
    restday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?"
    
    def __init__(self, params_dict):
        """
            생성자

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)

            Returns: 
                request_urls: 조회할 Request url 들의 list (list)

            Exception: 
        """
        base_url = self.restday_url
            
        super().__init__(url = base_url)
#         self.year = year
        self.params_dict = params_dict
        self.type = "xml"
        
    
    def create_request_urls(self, params_dict):
        """
            특정 년도의 전체 월을 조회하는 Request URL들을 list 형태로 생성하는 Method (Override)
            (휴일 데이터 API는 월별 조회만 가능)

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)

            Returns: 
                request_urls: 조회할 Request url 들의 list (list)

            Exception: 
        """
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
        """
            데이터를 가져오는 Method

            Args: 

            Returns: 
                API를 통해 가져온 DataFrame (Pandas.DataFrame)

            Exception: 
        """
        # 특정 월에 대해서 조회하는 경우 (solMonth가 params_dict에 존재하는 경우)는 url 1개만 생성
        # solMonth가 params_dict에 존재하지 않는 경우, 1월~12월까지를 조회할 수 있도록 request_urls 리스트를 생성
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
    """
        휴일 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            festival_data: 축제 데이터 (Pandas.DataFrame)

        Exception: 
    """
    holiday_api = Holiday_Data_by_API(params_dict = params_dict)
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
    
  
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *
from .Geocoding_by_API import *


class Trading_Area_Data_by_API(Data_by_API):
    """
        API를 통해 상권 데이터를 가져오는 Class
    """
    base_url = "http://apis.data.go.kr/B553077/api/open/sdsc/storeListInDong?" # JSON , XML
    
    def __init__(self, params_dict):
        """ls 
            Trading_Area_Data_by_API Class의 생성자

            Args: 
                params_dict : API 요청 파라미터 (Dictionary)
                
            Returns:
                
            Exception: 
        """

        super().__init__(url = self.base_url)
#         temp_geocode = get_geocode(city, google_key)
#         params_dict['cx'], params_dict['cy'] = temp_geocode['lng'], temp_geocode['lat']
#         self.cx = params_dict.get('cx')
#         self.cy = params_dict.get('cy')
        
        self.params_dict = params_dict  
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.type = params_dict.get("type")
    
    
    def calculate_max_page(self, type = "json"):
        """
            최대 Page 수를 찾는 Method
            (한 화면에 보여지는 Row 수(numofRows)에 따라서 전체 Page가 달라질 수 있으므로, 최대 Page를 찾은 후 해당 값만큼 Loop을 수행)

            Args: 
                type: json/xml 여부 (str) 

            Returns: 
                max_page: 최대 페이지 수 (int)

            Exception: 
        """
        rq = self.request()
        
        rq_dict = self.to_dict(txt = rq.text, type = type)
        
        self.n_rows = int(self.params_dict["numOfRows"])
        
        try:
            self.total_count = int(rq_dict["body"]["totalCount"])
        except:
            xmlsoup = BeautifulSoup(rq.text,'html.parser')
            self.total_count = int(xmlsoup.find("totalcount").text)
                
        max_page = int(np.ceil(self.total_count / self.n_rows))
        
        print(f"n_rows : {self.n_rows}, total_count : {self.total_count}, max_page = {max_page}")
        
        return max_page
        
        
    def extract_values_from_dict(self, dct):
        """
            Request Dictionary 로 부터 필요한 item들을 추출하는 Method (Override)

            Args: 
                dct: request 결과 Dictionary (dict)

            Returns: 
                dict_list: item들의 list (list)

            Exception: 
        """
        try: 
            dict_list = dct["body"]["items"]["item"]
        except:
            dict_list = dct["body"]["items"]
        
        return dict_list



def Load_Trading_Area_Data(params_dict,
#                            google_key,
#                            select_region = '',
                           save_tf = False, 
                           save_path = os.getcwd()):
    """
        상권 데이터를 가져오는 함수

        Args: 
            params_dict: API 요청 파라미터 (Dictionary)
            google_key: Google API Key (str)
            select_region: 지역명 (str)
            save_tf: 결과 저장 여부 (Bool)
            save_path: 결과 저장 경로 (str)

        Returns: 
            trading_area_data: 상권 데이터 (Pandas.DataFrame)

        Exception: 
    """
#     params_dict['google_key'] = google_key
#     params_dict['select_region'] = select_region
    
    trading_area_api = Trading_Area_Data_by_API(params_dict = params_dict)
    trading_area_data = trading_area_api.get()
        
    # index 초기화
    trading_area_data = trading_area_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        trading_area_data.to_csv(save_path +'/trading_area_data.csv', index=False)
    else :
        return trading_area_data
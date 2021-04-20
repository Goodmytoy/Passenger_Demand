  
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *
from .Geocoding_by_API import *


class Trading_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/B553077/api/open/sdsc/storeListInRadius?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        temp_geocode = get_geocode(params_dict.get('select_region'), params_dict.get('google_key'))
        params_dict['cx'], params_dict['cy'] = temp_geocode['lng'], temp_geocode['lat']
        self.cx = params_dict.get('cx')
        self.cy = params_dict.get('cy')
        
        del params_dict['select_region']
        del params_dict['google_key']
        
        self.params_dict = params_dict  
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.type = params_dict.get("type")
        
        
    def calculate_max_page(self, type = "json"):
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
        try: 
            dict_list = dct["body"]["items"]["item"]
        except:
            dict_list = dct["body"]["items"]
        
        return dict_list
    
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
    
    params_dict['google_key'] = google_key
    params_dict['select_region'] = select_region
    
    trading_api = Trading_Data_by_API(params_dict = params_dict)
    trading_data = trading_api.get()
        
    # index 초기화
    trading_data = trading_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        trading_data.to_csv(save_path +'/trading_data.csv', index=False)
    else :
        return trading_data
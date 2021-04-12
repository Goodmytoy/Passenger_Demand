import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *
from utils.Geocoding_by_API import *


class Trading_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/B553077/api/open/sdsc/storeOne?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        params_dict['cx'] = gmaps.geocode(params_dict.get('region'))[0]["geometry"]["location"]['lat']
        params_dict['cy'] = gmaps.geocode(params_dict.get('region'))[0]["geometry"]["location"]['lng']
        self.cx = params_dict.get('cx')
        self.cy = params_dict.get('cy')
        
        del params_dict['region']
        
        self.params_dict = params_dict  
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.type = params_dict.get("type")
        
    def create_request_url(self, params_dict):
#         params_dict["service_key"] = self.serviceKey
        params_list = [f"{k}={v}" for k, v in params_dict.items()]
        params_str = "&".join(params_list)
#         print(params_str)
        
        self.request_url = self.url + params_str
        print(self.request_url)
        return self.request_url
    
    def create_request_urls(self):
        max_page = self.calculate_max_page(type = self.type)
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["pageNo"] = i + 1
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

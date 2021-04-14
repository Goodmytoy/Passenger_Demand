import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *


class University_Data_by_API(Data_by_API):
    
    base_url = "http://www.career.go.kr/cnet/openapi/getOpenApi?" # JSON , XML
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("contentType")
    
    
    def extract_values_from_dict(self, dct):
        try: 
            dict_list = dct["dataSearch"]["content"]
        except:
            dict_list = dct["dataSearch"]["content"]
        
        return dict_list
    
    
    def create_request_urls(self):
        max_page = 1
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["thisPage"] = i + 1
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
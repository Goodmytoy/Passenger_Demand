import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *



class Weather_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?"
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["dataType"].lower()
    
    
    def get(self):
        
        self.request_urls = self.create_request_urls()

        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
            text_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in text_dict.items():
                data_dict[k].extend(v)
            
        return pd.DataFrame(data_dict)

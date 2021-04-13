import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
from utils.Data_by_API import *

class Holiday_Data_by_API(Data_by_API):
    
    holiday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo?"
    restday_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?"
    
    def __init__(self, params_dict, type):
        if type == "holi":
            base_url = self.holiday_url
        elif type == "rest":
            base_url = self.restday_url
            
        super().__init__(url = base_url)
#         self.year = year
        self.params_dict = params_dict
        self.type = "xml"
        
    
    def create_request_urls(self, params_dict):
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

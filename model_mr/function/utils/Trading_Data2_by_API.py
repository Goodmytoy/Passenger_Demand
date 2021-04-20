import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *


class Trading_Data2_by_API(Data_by_API):
    
    base_url = "http://www.localdata.go.kr/platform/rest/TO0/openDataApi?"
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict.get("resultType")
    
    def calculate_max_page(self, type = "json"):
        rq = self.request()
        
        rq_dict = self.to_dict(txt = rq.text, type = type)
        
        self.n_rows = int(self.params_dict["pageSize"])
        
        try:
            self.total_count = int(rq_dict["result"]["header"]["paging"]["totalCount"])
        except:
            xmlsoup = BeautifulSoup(rq.text,'html.parser')
            self.total_count = int(xmlsoup.find("totalCount").text)
                
        max_page = int(np.ceil(self.total_count / self.n_rows))
        
        print(f"n_rows : {self.n_rows}, total_count : {self.total_count}, max_page = {max_page}")
        
        return max_page
    
    
    def extract_values_from_dict(self, dct): 
        dict_list = dct["result"]["body"]["rows"][0]["row"]
            
        return dict_list
    
    def create_request_urls(self):
        max_page = self.calculate_max_page(type = self.type)
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["pageIndex"] = i + 1
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

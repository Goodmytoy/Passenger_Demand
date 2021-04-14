import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *


class School_Data_by_API(Data_by_API):
    
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_elesch_mskul_lc_api?"
    
    def __init__(self, params_dict):
        """
            School_Data_by_API Class의 생성자

            Args: 
                params_dict : API Request Parameters (Dictionary)
                
            Returns:
                
            Exception: 
        """
        
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["type"]
  
    
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
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
#             temp_dict = self.parse_json(request = rq, features = None)
            temp_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
        
    
        return pd.DataFrame(data_dict)
import pandas as pd
import numpy as np
from collections import defaultdict
from utils.Data_by_API import *



class Weather_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?"
    
    def __init__(self, params_dict, url = base_url):
        super().__init__(url, params_dict)
        super().create_request_url()
        
        
    def calculate_max_page(self):
        rq = super().request()
        
        self.n_rows = int(self.params_dict["numOfRows"])
        self.total_count = rq.json()["response"]["body"]["totalCount"]
        
        max_page = int(np.ceil(self.total_count / self.n_rows))
        
        print(f"n_rows : {self.n_rows}, total_count : {self.total_count}, max_page = {max_page}")
        
        return max_page
    
    def get(self):
        rq = super().request()
        
        max_page = self.calculate_max_page()
        
        output_cols = rq.json()["response"]["body"]["items"]["item"][0].keys()
        
        data_dict = defaultdict(list)
        for i in range(max_page):
            
            self.params_dict["pageNo"] = i + 1
            super().create_request_url()
            rq = super().request()
            json_list = rq.json()["response"]["body"]["items"]["item"]
                                                               
            for js in json_list:
                for col in output_cols:
                    data_dict[col].append(js[col])
                    
        return pd.DataFrame(data_dict)
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from .Data_by_API import *


class PM_Data_by_API(Data_by_API):
    
    base_url = "http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo?"
    
    def __init__(self, params_dict):
        super().__init__(url = self.base_url)
        self.request_url = super().create_request_url(params_dict = params_dict)
        self.params_dict = params_dict
        self.type = params_dict["returnType"]
        
      
    
    def parse_json(self, request, features = None):
        data_dict = defaultdict(list)
        rq_json = request.json()
        
        if features is None:
            features = rq_json["response"]["body"]["items"][0].keys()
        
        json_list = rq_json["response"]["body"]["items"]                                                          
        for js in json_list:
            for col in features:
                data_dict[col].append(js[col])
        
        return data_dict
    
    
    def get(self):
        
        self.request_urls = self.create_request_urls()
        
        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            rq = self.request(request_url = request_url)
#             temp_dict = self.parse_json(request = rq, features = None)
            temp_dict = self.parse(request = rq, features = None, type = self.type)
            
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
            
        return pd.DataFrame(data_dict)
    
    
    

def Load_Particulate_Matter_Data(params_dict,
                                 save_tf = False, 
                                 save_path = os.getcwd()):
    
    pm_api = PM_Data_by_API(params_dict = params_dict)
    pm_data = pm_api.get()
    
    # index 초기화
    pm_data = pm_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        pm_data.to_csv(save_path +'/pm_data.csv', index=False)
    else :
        return pm_data
    
# -*- coding: utf-8 -*-
from utils.Trading_Data_by_API import *
import os

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

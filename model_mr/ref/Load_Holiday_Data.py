# -*- coding: utf-8 -*-
from utils.Holiday_Data_by_API import *
import os

def Load_Holiday_Data(params_dict,
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    holiday_api = Holiday_Data_by_API(params_dict = params_dict, type = "rest")
    holiday_data = holiday_api.get()
    
    # index 초기화
    holiday_data = holiday_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        holiday_data.to_csv(save_path +'/holiday_data.csv', index=False)
    else :
        return holiday_data

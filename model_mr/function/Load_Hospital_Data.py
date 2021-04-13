# -*- coding: utf-8 -*-
from utils.Hospital_Data_by_API import *
import os

def Load_Hospital_Data(params_dict,
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    hospital_api = Hospital_Data_by_API(params_dict = params_dict)
    hospital_data = hospital_api.get()
    
    
    # index 초기화
    hospital_data = hospital_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        hospital_data.to_csv(save_path +'/hospital_data.csv', index=False)
    else :
        return hospital_data

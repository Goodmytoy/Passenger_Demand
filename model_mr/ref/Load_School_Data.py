# -*- coding: utf-8 -*-
from utils.School_Data_by_API import *
import os

def Load_School_Data(params_dict,
                     select_region = '',
                     save_tf = False, 
                     save_path = os.getcwd()):
    
    school_api = School_Data_by_API(params_dict = params_dict)
    school_data = school_api.get()
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        school_data = school_data.loc[school_data["rdnmadr"].str.contains(select_region)]
        
    # index 초기화
    school_data = school_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        school_data.to_csv(save_path +'/school_data.csv', index=False)
    else :
        return school_data

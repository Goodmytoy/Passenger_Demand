# -*- coding: utf-8 -*-
##########################################
# 상권데이터 수집
# #########################################
from utils.Trading_Data2_by_API import *
from utils.Geocoding_by_API import *
import os

def Load_Trading_Data2(params_dict,
                      google_key,
                      select_region = '', 
                      save_tf = False, 
                      save_path = os.getcwd()):
    
    trading_api = Trading_Data2_by_API(params_dict = params_dict)
    trading_data2 = trading_api.get()
    
    # 날짜데이터 형변환
    trading_data2["updateDt"] = pd.to_datetime(trading_data2["updateDt"], format = "%Y-%m-%d")
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        trading_data2 = trading_data2.loc[trading_data2["siteWhlAddr"].str.contains(select_region)]
    
    # Geocoding
    trading_data2 = get_geocodeDf(trading_data2, "rdnWhlAddr", google_key)
    
    # index 초기화
    trading_data2 = trading_data2.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        trading_data2.to_csv(save_path +'/trading_data2.csv', index=False)
    else :
        return trading_data2

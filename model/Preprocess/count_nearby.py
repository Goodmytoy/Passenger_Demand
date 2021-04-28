from haversine import *
import pandas as pd
import numpy as np


def count_nearby(data, 
                 nearby_data, 
                 col_nm, 
                 dist = 0.2, 
                 category_list = None):
    """
        근처 카테고리들의 개수를 산출하여 변수로 추가하는 함수

        Args: 
            data: 데이터 (Pandas.DataFrame)
            nearby_data: 지역 정보 데이터 (Pandas.DataFrame)
            col_nm: 결과 컬럼명 (str)
            dist: 거리 (Float)
            category_list: 카테고리 리스트 (list)

        Returns: 
            data_copy: 결과 데이터 (Pandas.DataFrame)

        Exception: 
    """

    data_copy = data.copy()
    
    # 주변 위치들과 정류장 간의 거리 산출 (Haversine 거리)
    dist_list = nearby_data[["latitude", "longitude"]].apply(lambda x: haversine((x["latitude"], x["longitude"]), (data_copy["latitude"], data_copy["longitude"])), 1)
    
    within_data = nearby_data.loc[dist_list <= dist]
    
    for i, ctgr in enumerate(category_list):
        data_copy[f"{col_nm}_{i}"] = (within_data["category"] == ctgr).sum()
    
    return data_copy


def count_time_nearby(data, 
                      date_col, 
                      nearby_data, 
                      col_nm, 
                      dist = 0.2):
    """
        특정 기간 내에 근처 카테고리들의 개수를 산출하여 변수로 추가하는 함수

        Args: 
            data: 데이터 (Pandas.DataFrame)
            nearby_data: 지역 정보 데이터 (Pandas.DataFrame)
            col_nm: 결과 컬럼명 (str)
            dist: 거리 (Float)
            category_list: 카테고리 리스트 (list)

        Returns: 
            data_copy: 결과 데이터 (Pandas.DataFrame)

        Exception: 
    """
    data_copy = data.copy()
    within_data = nearby_data.loc[(nearby_data["startDate"] <= data_copy[date_col]) & (nearby_data["endDate"] >= data_copy[date_col])]
    
    if len(within_data) == 0:
        data_copy[f"{col_nm}_nearby"] = 0
    else:
        dist_list = within_data[["latitude", "longitude"]].apply(lambda x: haversine((x["latitude"], x["longitude"]), (data_copy["latitude"], data_copy["longitude"])), 1)
        data_copy[f"{col_nm}_nearby"] = (dist_list <= dist).sum()

    return data_copy
from haversine import *
import pandas as pd
import numpy as np


def count_nearby(data, nearby_data, col_nm, dist = 0.2, category_list = None):
    data_copy = data.copy()
    
    # 주변 위치들과 정류장 간의 거리 산출 (Haversine 거리)
    dist_list = nearby_data[["latitude", "longitude"]].apply(lambda x: haversine((x["latitude"], x["longitude"]), (data_copy["latitude"], data_copy["longitude"])), 1)
    
    within_data = nearby_data.loc[dist_list <= dist]
    
    for i, ctgr in enumerate(category_list):
        data_copy[f"{col_nm}_{i}"] = (within_data["category"] == ctgr).sum()
    
    return data_copy


def count_time_nearby(data, date_col, nearby_data, col_nm, dist = 0.2):
    data_copy = data.copy()
    within_data = nearby_data.loc[(nearby_data["startDate"] <= data_copy[date_col]) & (nearby_data["endDate"] >= data_copy[date_col])]
    
    if len(within_data) == 0:
        data_copy[f"{col_nm}_nearby"] = 0
    else:
        dist_list = within_data[["latitude", "longitude"]].apply(lambda x: haversine((x["latitude"], x["longitude"]), (data_copy["latitude"], data_copy["longitude"])), 1)
        data_copy[f"{col_nm}_nearby"] = (dist_list <= dist).sum()

    return data_copy
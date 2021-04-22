import pandas as pd
import numpy as np


def preprocessing_trading_area_data(trading_area_data):
    
    # trading_area_data = trading_area_data[["상호명", "상권업종중분류명", "도로명주소", "위도", "경도"]]
    # trading_area_data = trading_area_data.rename(columns = {"상호명" : "name",
    #                                                         "상권업종중분류명" : "category",
    #                                                         "도로명주소" : "addr",
    #                                                         "위도" : "latitude",
    #                                                         "경도" : "longitude"})
    
    trading_area_data = trading_area_data[["bizesNm", "indsMclsNm", "rdnm", "lat", "lon"]]
    trading_area_data = trading_area_data.rename(columns = {"bizesNm" : "name",
                                                            "indsMclsNm" : "category",
                                                            "rdnm" : "addr",
                                                            "lat" : "latitude",
                                                            "lon" : "longitude"})
    return trading_area_data
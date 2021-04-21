# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def preprocessing_trading_area_data(trading_area_data):
    
    trading_area_data = trading_area_data[['bizesNm', 'indsMclsNm', 'rdnmAdr', 'lat', 'lon']]
                                       # "상호명","상권업종중분류명","도로명주소","위도","경도"]]
    trading_area_data = trading_area_data.rename(columns = {"bizesNm" : "name",
                                                            "indsMclsNm" : "category",
                                                            "rdnmAdr" : "addr",
                                                            "lat" : "latitude",
                                                            "lon" : "longitude"})
    
    return trading_area_data

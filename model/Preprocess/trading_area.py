import pandas as pd
import numpy as np


def preprocessing_trading_area_data(trading_area_data):
    """
        상권 데이터를 전처리 하는 함수
        
        Args: 
            trading_area_data: 상권 데이터 (Pandas.DataFrame)

        Returns: 
            trading_area_data: 상권 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # 필요한 컬럼 추출
    trading_area_data = trading_area_data[["bizesNm", "indsMclsNm", "rdnm", "lat", "lon"]]
    trading_area_data = trading_area_data.rename(columns = {"bizesNm" : "name",
                                                            "indsMclsNm" : "category",
                                                            "rdnm" : "addr",
                                                            "lat" : "latitude",
                                                            "lon" : "longitude"})
    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)  
    trading_area_data["longitude"] = trading_area_data["longitude"].astype(float)
    trading_area_data["latitude"] = trading_area_data["latitude"].astype(float)

    return trading_area_data
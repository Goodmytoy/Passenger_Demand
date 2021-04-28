import pandas as pd
import numpy as np


def preprocess_festival_data(festival_data, 
                             start_date, 
                             end_date):
    """
        축제 데이터 전처리 함수

        Args: 
            festival_data: 축제 데이터 (Pandas.DataFrame)
            start_date: 시작 일자 (str)
            end_date: 종료 일자 (str)

        Returns: 
            festival_data: 축제 데이터 (Pandas.DataFrame)

        Exception: 
    """
    # 날짜 컬럼으로 변환
    festival_data["startDate"] = pd.to_datetime(festival_data["fstvlStartDate"])
    festival_data["endDate"] = pd.to_datetime(festival_data["fstvlEndDate"])
    
    # 필요한 컬럼 추출
    festival_data = festival_data[["fstvlNm", "rdnmadr", "startDate", "endDate", "latitude", "longitude"]]
    # (start_date, end_date) 범위 사이의 데이터만 추출
    festival_data = festival_data.loc[festival_data["startDate"].dt.date.between(pd.to_datetime(start_date).date(), 
                                                                                 pd.to_datetime(end_date).date())].reset_index(drop = True)

    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)    
    festival_data["longitude"] = festival_data["longitude"].astype(float)
    festival_data["latitude"] = festival_data["latitude"].astype(float)

    return festival_data
    

import pandas as pd
import numpy as np

def preprocessing_school_data(school_data):
    """
        학교(초중고) 데이터를 전처리 하는 함수
        
        Args: 
            school_data: 학교(초중고) 데이터 (Pandas.DataFrame)

        Returns: 
            school_data: 학교(초중고) 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # 필요한 컬럼 추출
    school_data = school_data[["schoolNm", "schoolSe", "rdnmadr", "latitude", "longitude"]]
    school_data = school_data.rename(columns = {"schoolNm" : "name",
                                                "schoolSe" : "category",
                                                "rdnmadr" : "addr"})
    
    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)   
    school_data["longitude"] = school_data["longitude"].astype(float)
    school_data["latitude"] = school_data["latitude"].astype(float)

    return school_data
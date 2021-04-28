
import pandas as pd
import numpy as np

def preprocessing_university_data(university_data):
    """
        대학교 데이터를 전처리 하는 함수
        
        Args: 
            university_data: 대학교 데이터 (Pandas.DataFrame)

        Returns: 
            university_data: 대학교 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # 필요한 컬럼 추출
    university_data = university_data[["schoolName", "schoolGubun", "adres", "latitude", "longitude"]]
    university_data = university_data.rename(columns = {"schoolName" : "name",
                                                        "schoolGubun" : "category",
                                                        "adres" : "addr"})

    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)  
    university_data["longitude"] = university_data["longitude"].astype(float)
    university_data["latitude"] = university_data["latitude"].astype(float)

    return university_data
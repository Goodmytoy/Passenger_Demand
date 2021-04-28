import pandas as pd
import numpy as np

def preprocessing_hospital_data(hospital_data):
    """
        병원 데이터 전처리 함수

        Args: 
            hospital_data: 병원 데이터 (Pandas.DataFrame)

        Returns: 
            hospital_data: 병원 데이터 (Pandas.DataFrame)

        Exception: 
    """
    # 병원 카테고리 변환
    hospital_data["category"] = hospital_data["clCdNm"].replace({"한방병원" : "병원",
                                                                 "치과병원" : "병원",
                                                                 "정신병원" : "병원",
                                                                 "상급종합" : "종합병원",
                                                                 "부속의원" : "의원",
                                                                 "치과의원" : "의원",
                                                                 "한의원" : "의원",
                                                                 "보건진료소" : "보건소",
                                                                 "보건지소" : "보건소"})
    # 필요한 컬럼 추출
    hospital_data = hospital_data[["addr", "category", "XPos", "YPos"]]
    hospital_data = hospital_data.rename(columns = {"XPos" : "longitude",
                                                    "YPos" : "latitude"})

    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)    
    hospital_data["longitude"] = hospital_data["longitude"].astype(float)
    hospital_data["latitude"] = hospital_data["latitude"].astype(float)
    
    return hospital_data
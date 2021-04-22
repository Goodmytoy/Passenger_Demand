import pandas as pd
import numpy as np

def preprocessing_hospital_data(hospital_data):
    hospital_data["category"] = hospital_data["clCdNm"].replace({"한방병원" : "병원",
                                                                 "치과병원" : "병원",
                                                                 "정신병원" : "병원",
                                                                 "상급종합" : "종합병원",
                                                                 "부속의원" : "의원",
                                                                 "치과의원" : "의원",
                                                                 "한의원" : "의원",
                                                                 "보건진료소" : "보건소",
                                                                 "보건지소" : "보건소"})
    
    hospital_data = hospital_data[["addr", "category", "XPos", "YPos"]]
    hospital_data = hospital_data.rename(columns = {"XPos" : "longitude",
                                                    "YPos" : "latitude"})

    hospital_data["longitude"] = hospital_data["longitude"].astype(float)
    hospital_data["latitude"] = hospital_data["latitude"].astype(float)
    
    return hospital_data
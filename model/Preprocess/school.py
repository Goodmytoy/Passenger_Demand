# def preprocessing_school_data(school_data):    
#     school_data = school_data[["schoolNm", "schoolSe", "rdnmadr", "latitude", "longitude"]]
#     school_data = school_data.rename(columns = {"schoolNm" : "name",
#                                                 "schoolSe" : "category",
#                                                 "rdnmadr" : "addr"})
    
#     return school_data
import pandas as pd
import numpy as np


def preprocessing_school_data(school_data): 
    school_data["category"] = school_data["학교종류"].replace({"전문대학(3년제)" : "전문대학",
                                                              "사내대학(전문)" : "전문대학",
                                                              "기능대학" : "전문대학",
                                                              "일반대학원" : "대학원",
                                                              "전문대학원" : "대학원",
                                                              "특수대학원" : "대학원",
                                                              "일반고등학교" : "고등학교",
                                                              "공업고등학교" : "고등학교",
                                                              "상업고등학교" : "고등학교",
                                                              "가사고등학교" : "고등학교",
                                                              "체육고등학교" : "고등학교",
                                                              "외국어고등학교" : "고등학교",
                                                              "과학고등학교" : "고등학교",
                                                              "예술고등학교" : "고등학교"})
    
    school_data = school_data[["학교명", "category", "지번주소", "latitude", "longitude"]]
    school_data = school_data.rename(columns = {"학교명" : "name",
                                                "지번주소" : "addr"})
    
    return school_data
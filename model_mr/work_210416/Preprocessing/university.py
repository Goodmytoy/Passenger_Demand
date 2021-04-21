import pandas as pd
import numpy as np

def preprocessing_university_data(university_data): 
    university_data["category"] = university_data["schoolType"].fillna('일반대학').replace({"각종대학(대학)" : "일반대학",
                                                                                        "교육대학" : "일반대학",
                                                                                        "사이버대학(4년제)" : "사이버대학",
                                                                                        "사이버대학(2년제)" : "사이버대학",
                                                                                        "산업대학" : "전문대학",
                                                                                        "기능대학(폴리텍대학)" : "전문대학"})
    
    university_data = university_data[["schoolName", "category", "adres", "latitude", "longitude"]]
    university_data = university_data.rename(columns = {"schoolName" : "name",
                                                "adres" : "addr"})
    
    return university_data


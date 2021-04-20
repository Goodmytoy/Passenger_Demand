
import pandas as pd
import numpy as np

def preprocessing_university_data(university_data):    
    university_data = university_data[["schoolName", "schoolGubun", "adres", "latitude", "longitude"]]
    university_data = university_data.rename(columns = {"schoolName" : "name",
                                                        "schoolGubun" : "category",
                                                        "adres" : "addr"})

    university_data["longitude"] = university_data["longitude"].astype(float)
    university_data["latitude"] = university_data["latitude"].astype(float)

    return university_data
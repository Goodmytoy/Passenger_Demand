import pandas as pd
import numpy as np


def preprocess_festival_data(festival_data, start_date, end_date):
    
    festival_data["startDate"] = pd.to_datetime(festival_data["fstvlStartDate"])
    festival_data["endDate"] = pd.to_datetime(festival_data["fstvlEndDate"])
    
    festival_data = festival_data[["fstvlNm", "rdnmadr", "startDate", "endDate", "latitude", "longitude"]]
    festival_data = festival_data.loc[festival_data["startDate"].dt.date.between(pd.to_datetime(start_date).date(), 
                                                                                 pd.to_datetime(end_date).date())].reset_index(drop = True)
    
    return festival_data
    
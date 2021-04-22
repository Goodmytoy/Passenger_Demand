import pandas as pd
import numpy as np

def preprocess_event_data(event_data, start_date, end_date):
    
    event_data["eventStartTime"] = (event_data["eventStartTime"].str.extract(r"(\d+):")[0]
                                                                .str.pad(width=2, side='left', fillchar='0')
                                                                .replace({"24":"23"}))
    event_data["eventEndTime"] = (event_data["eventEndTime"].str.extract(r"(\d+):")[0]
                                                            .str.pad(width=2, side='left', fillchar='0')
                                                            .replace({"24":"23"}))
    
    event_data["startDate"] = pd.to_datetime(event_data["eventStartDate"].dt.strftime("%Y-%m-%d") + " " + event_data["eventStartTime"], format = "%Y-%m-%d %H")
    event_data["endDate"] = pd.to_datetime(event_data["eventEndDate"].dt.strftime("%Y-%m-%d") + " " + event_data["eventEndTime"], format = "%Y-%m-%d %H")
    
    event_data = event_data[["eventNm", "rdnmadr", "startDate", "endDate", "latitude", "longitude"]]
    event_data = event_data.loc[event_data["startDate"].dt.date.between(pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date())].reset_index(drop = True)
    
    event_data["longitude"] = event_data["longitude"].astype(float)
    event_data["latitude"] = event_data["latitude"].astype(float)

    return event_data
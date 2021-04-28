import pandas as pd
import numpy as np

def preprocess_pm_data(pm_data, 
                       city = "울산"):
    """
        미세먼지 경보 데이터를 전처리 하는 함수
        
        Args: 
            pm_data: 날씨 데이터 (Pandas.DataFrame)
            city: 도시명 (str)
            
        Returns: 
            data: 미세먼지 경보 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # 날짜 형태 변환
    pm_data["issueDate"] = pd.to_datetime(pm_data["issueDate"], format = "%Y-%m-%d")
    
    # 일별 경보 횟수의 합계 데이터 생성
    pm_data_agg = pm_data.loc[pm_data["districtName"] == city].groupby(pd.Grouper(key="issueDate", freq="1D")).size().reset_index(name = "pm_alert_cnt")
    
    pm_data_agg["date"] = pm_data_agg["issueDate"].dt.date
    pm_data_agg = pm_data_agg.drop("issueDate", 1)
    
    
    # 전체 일자 생성
    start_year = pm_data["issueDate"].dt.year.min()
    end_year = pm_data["issueDate"].dt.year.max()
    
    date_df = pd.DataFrame({"date" : pd.date_range(f"{start_year}-01-01", f"{end_year}-12-31", freq = "1D")})
    date_df["date"] = date_df["date"].dt.date
    date_df = pd.merge(date_df, pm_data_agg, on = "date", how = "left").fillna(0)
    
    
    return date_df
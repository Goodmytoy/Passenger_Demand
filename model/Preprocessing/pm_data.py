def preprocess_pm_data(pm_data, date_col = "issueDate", city = "울산"):
    """
        미세먼지 경보 데이터를 전처리 하는 함수
        
        Args: 
            pm_data: 날씨 데이터 (Pandas.DataFrame)
            date_col: date_col: 날짜 컬럼명 (str)
            city: 도시명 (str)
            
        Returns: 
            data: 미세먼지 경보 데이터를 전처리한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    pm_data[date_col] = pd.to_datetime(pm_data[date_col], format = "%Y-%m-%d")
    pm_data_agg = pm_data.loc[pm_data["districtName"] == city].groupby(pd.Grouper(key=date_col, freq="1D")).size().reset_index(name = "pm_alert_cnt")
    
    pm_data_agg["date"] = pm_data_agg[date_col].dt.date
    pm_data_agg = pm_data_agg.drop(date_col, 1)
    
    
    # 전체 일자 생성
    start_year = pm_data[date_col].dt.year.min()
    end_year = pm_data[date_col].dt.year.max()
    
    date_df = pd.DataFrame({"date" : pd.date_range(f"{start_year}-01-01", f"{end_year}-12-31", freq = "1D")})
    date_df["date"] = date_df["date"].dt.date
    date_df = pd.merge(date_df, pm_data_agg, on = "date", how = "left").fillna(0)
    
    
    return date_df
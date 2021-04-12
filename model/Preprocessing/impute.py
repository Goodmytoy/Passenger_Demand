def impute_recent_data(data, 
                       missing_date, 
                       date_col = "transdate"):
    """
        n주 전 같은 요일 같은 시간대의 인원 수로 Impute

        Args: 
            data: 데이터 (Pandas.DataFrame)
            missing_date: 결측일의 리스트 (list)
            date_col: 날짜 컬럼명 (str)

        Returns: 
            data: 결측일의 데이터를 Impute한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """    
    data = data.copy()
    for x in missing_date:
        temp = []
        w = 0
        while len(temp) == 0:
            w +=1
            temp = data.loc[data[date_col].dt.date == (x - timedelta(weeks = w)).date()].copy()

        temp[date_col] = temp[date_col] + timedelta(weeks = w)
        data = pd.concat([data, temp], 0)
        
    return data



# 최근 n주의 같은 요일 같은 시간대의 평균값으로 Impute
def impute_recent_mean_data(data, 
                            missing_date, 
                            date_col):
    """
        최근 n주의 같은 요일 같은 시간대의 평균값으로 Impute

        Args: 
            data: 데이터 (Pandas.DataFrame)
            missing_date: 결측일의 리스트 (list)
            date_col: 날짜 컬럼명 (str)

        Returns: 
            data: 결측일의 데이터를 Impute한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """ 
    
    data = data.copy()

    # 요일, 시간 추가
    data["dayofweek"] = data["transdate"].dt.dayofweek
    dow_dict = {0:"월", 1:"화", 2:"수", 3:"목", 4:"금", 5:"토", 6:"일"}
    data["dayofweek"] = data["dayofweek"].replace(dow_dict)
    data["hour"] = data["transdate"].dt.hour
         
    
    for x in missing_date:
        base_date = x
        w = 0
        # 결측일의 이전 4주를 기본으로 검색하며, 데이터가 없는 경우 범위를 1주씩 늘려가며 데이터 조회
        temp = []
        while len(temp) == 0:
            temp = data.loc[(data["transdate"].dt.date.between((x - timedelta(weeks = 4+w)).date(), x.date())) & 
                            (data["transdate"].dt.dayofweek == x.day_of_week)].copy()
            w += 1

        # 4+w 전까지의 데이터를 찾아서 정류장별, 요일별, 시간별 평균값 산출
        temp2 = temp.groupby(["mybi_stop_id", "dayofweek", "hour"]).agg({"totalcnt" : np.mean,
                                                                         "normalcnt" : np.mean,
                                                                         "studentcnt" : np.mean,
                                                                         "childcnt" : np.mean}).reset_index()
        # 평균값 변환 (Float -> Int : 반올림 효과)
        temp2["totalcnt"] = temp2["totalcnt"].astype(int)
        temp2["normalcnt"] = temp2["normalcnt"].astype(int)
        temp2["studentcnt"] = temp2["studentcnt"].astype(int)
        temp2["childcnt"] = temp2["childcnt"].astype(int)

        # 기준 일자, 시간으로 부터 transdate을 재생성
        temp2["transdate"] = temp2.apply(lambda x: base_date + timedelta(hours = x["hour"]), 1)

        data = pd.concat([data, temp2], 0)
        
    return data



def impute_bus_demand_data(data, 
                           date_col, 
                           stop_id_col):
    """
        결측일과 결측치(카드 정보가 존재하지 않는 시간대)를 Impute
        
        Args: 
            data: 데이터 (Pandas.DataFrame)
            date_col: 날짜 컬럼명 (str)
            stop_id_col: 정류장 컬럼명 (str)

        Returns: 
            data: 결측일과 결측치(카드 정보가 존재하지 않는 시간대)를 Impute한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # 일 단위 집계 -> 데이터가 존재하지 않는 일은 결측일로 판단 (missing_date)
    count_by_date = data.groupby([pd.Grouper(key=date_col, freq="1D")]).size().reset_index(name = "cnt")
    missing_date = count_by_date.loc[count_by_date["cnt"] == 0, date_col]
    
    # 1) 결측일을 제외한 결측치(데이터가 존재하지 않는 시간대)는 승객이 0명 이므로 0으로 대체
    data = data.loc[data[date_col].dt.date.isin(missing_date.dt.date) == False].fillna(0)
    
    # 2) 최근 n주의 같은 요일 같은 시간대의 평균값으로 Impute
    data = impute_recent_mean_data(data = data, missing_date = missing_date, date_col = "transdate")
    
    return data
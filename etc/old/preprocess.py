
def preprocess(data, date_col, target_cols, stop_id_col, num_cores = 12):
    data = data.copy()

    data = add_time_features(data = data, date_col = date_col)
    # 모든 시간대의 데이터로 변환
    all_date = create_all_date(data = data, date_col = date_col, stop_id_col = stop_id_col, except_hours=[1,2,3,4])

    # 일자별 Sum 데이터
    # 사용 : 날자별 Sum Lag 변수, 
    data_agg_daily_sum = create_data_agg(data = all_date, 
                                          date_col = date_col, 
                                          stop_id_col = stop_id_col, 
                                          target_cols = target_cols, 
                                          freq = "1D", 
                                          agg_func = sum)
    data_agg_daily_sum = add_time_features(data_agg_daily_sum, date_col = date_col)                                          


    # 시간 변수 생성(시간, 요일, 날짜, 주, 월)
    all_date = add_time_features(data = all_date, date_col = date_col)


    ######## 1. 결측치 Impute ########
    print("1. 결측치 Impute ... ", end = "")
    # 결측치
    all_date = impute_bus_demand_data(data = all_date, date_col = date_col, stop_id_col = stop_id_col)
    print(f"Finished ({all_date.shape})")

    ######## 2. 시계열 변수 생성(Lag 변수, MV 변수) ########
    print("2. 시계열 변수 생성 ... ")
    target_cols = ["totalcnt"]
    lags = ["1d", "2d", "3d", "4d", "5d", "6d", "7d"]
    
    # 2.1) Lags
    # 2.1.1) 동일 시간대 Lag 변수
    all_date = create_lag_feature(data = all_date, 
                                  target_cols = target_cols,  # "totalcnt", "normalcnt", "studentcnt", "childcnt"
                                  date_col = date_col, 
                                  lags = lags, 
                                  groupby_cols = stop_id_col)

    # 2.1.2) 날자별 sum Lag 변수
    daily_lag = create_lag_feature(data = data_agg_daily_sum, 
                                   target_cols = target_cols, 
                                   date_col = date_col, 
                                   lags = lags, 
                                   groupby_cols = stop_id_col)
    rename_dict = {f"{col}_bf_{lg}": f"{col}_bf_{lg}_total" for col in target_cols for lg in lags}
    daily_lag = daily_lag.rename(columns = rename_dict)

    daily_lag["date"] = daily_lag["transdate"].dt.date
    all_date = pd.merge(all_date, daily_lag[["date", stop_id_col] + list(rename_dict.values())], on = ["date", stop_id_col], how = "left")


    # 2.2) Moving Aggregation
    # 2,2.1) 이전 n개 인자들의 동일 시간대 평균
    all_date = calculate_moving_agg(data = all_date, 
                                    target_cols = target_cols, 
                                    date_col = date_col, 
                                    groupby_cols = [stop_id_col, "hour"], 
                                    col_nm = "hour", 
                                    rollings = ["2d", "3d", "4d", "5d", "6d"])
    
    # 2.2.2) n주 전까지의 동일 요일의 동일 시간대 평균
    all_date = calculate_moving_agg(data = all_date, 
                                    target_cols = target_cols, 
                                    date_col = date_col, 
                                    groupby_cols = [stop_id_col, "hour", "dayofweek"], 
                                    col_nm = "hour_week", 
                                    rollings = ["14d", "21d", "28d"])

    # 2.2.3) 이전 n개 일자들의 전체 평균
    daily_mv_agg = calculate_moving_agg(data = data_agg_daily_sum, 
                                        target_cols = target_cols, 
                                        date_col = date_col, 
                                        groupby_cols = stop_id_col, 
                                        col_nm = "daily", 
                                        rollings = ["2d", "3d", "4d", "5d", "6d"])
                                        
    daily_mv_agg["date"] = daily_mv_agg[date_col].dt.date

    # 불필요한 컬럼 제거
    drop_cols = [date_col, "dayofweek", "hour", "month", "weekofyear"]
    if isinstance(target_cols, list):
        drop_cols.extend(target_cols)
    elif isinstance(target_cols, str):
        drop_cols.append(target_cols)

    daily_mv_agg = daily_mv_agg.drop(drop_cols, 1)

    # Feature 추가
    all_date = pd.merge(all_date, daily_mv_agg, on = [stop_id_col, "date"], how = "left")

    # 2.2.4) 4주 전까지의 동일 요일의 전체 평균
    daily_week_mv_agg = calculate_moving_agg(data = data_agg_daily_sum, 
                                             target_cols = target_cols, 
                                             date_col = date_col, 
                                             groupby_cols = [stop_id_col, "dayofweek"], 
                                             col_nm = "daily_week", 
                                             rollings = ["14d", "21d", "28d"])
    daily_week_mv_agg["date"] = daily_week_mv_agg["transdate"].dt.date
    
    # 불필요한 컬럼 제거
    drop_cols = ["dayofweek", "hour", "month", "weekofyear"]
    if isinstance(target_cols, list):
        drop_cols.extend(target_cols)
    elif isinstance(target_cols, str):
        drop_cols.append(target_cols)
    
    daily_week_mv_agg = daily_week_mv_agg.drop(["transdate","totalcnt", "dayofweek", "hour", "month", "weekofyear"], 1)
    
    # Feature 추가
    all_date = pd.merge(all_date, daily_week_mv_agg, on = ["stop_id", "date"], how = "left")


    # 2.2.5) n주 전까지의 일별 합계의 주 단위 평균의 이동평균
    data_agg_weekly_mean = create_data_agg(data_agg_daily_sum,
                                           date_col = date_col, 
                                           stop_id_col = stop_id_col, 
                                           groupby_cols = "weekofyear",  
                                           target_cols = target_cols, 
                                           agg_func = np.mean)

    weekly_mv_agg = calculate_moving_agg(data = data_agg_weekly_mean, 
                                         target_cols = target_cols, 
                                         date_col = "weekofyear", 
                                         groupby_cols = stop_id_col, 
                                         col_nm = "weekly", 
                                         rollings = [2,3,4])
    #  불필요한 컬럼 제거
    weekly_mv_agg = weekly_mv_agg.drop(target_cols, 1)

    # Feature 추가
    all_date = pd.merge(all_date, weekly_mv_agg, on = [stop_id_col, "weekofyear"], how = "left")
    print(f"Finished ({all_date.shape})")


    ######## 3. 시간적 특성 변수 추가 (특일, 날씨, 미세먼지 경보) ########
    print("3. 시간적 특성 변수 추가 (특일, 날씨, 미세먼지 경보) ... ")
    # 3.1) 특일 데이터 변수 추가
    holiday_data = pd.read_parquet("/home/seho/Passenger_Demand/data/holiday_data.parquet")
    holiday_data = preprocess_holiday_data(holiday_data = holiday_data)
    all_date = pd.merge(all_date, holiday_data, how = "left", on = "date")

    # 3.2) 날씨 데이터 변수 추가
    weather_data = pd.read_parquet("/home/seho/Passenger_Demand/data/weather_2018.parquet")
    weather_data = preprocess_weather_data(weather_data = weather_data)
    all_date["time_hours"] = all_date[date_col].dt.strftime("%Y-%m-%d %H")
    all_date = pd.merge(all_date, weather_data, how = "left", on = "time_hours")
    all_date = all_date.drop(["time_hours"], 1)

    # 3.3) 미세먼지 경보 데이터 추가
    pm_data = pd.read_csv("/home/seho/Passenger_Demand/data/pm_data.csv")
    pm_data = preprocess_pm_data(pm_data = pm_data)
    all_date = pd.merge(all_date, pm_data, how = "left", on = "date")

    print(f"Finished ({all_date.shape})")

    ######## 4. 공간적 특성 정보 추가 (상권정보, 학교정보, 병원정보) ########
    print("4. 공간적 특성 정보 추가 (상권정보, 학교정보, 병원정보) ... ")
    # 정류장명, 정류장ID, 위도, 경도 정보
    bus_stop_info = data[[stop_id_col, "stop_nm", "longitude", "latitude"]].drop_duplicates().reset_index(drop = True)

    # 4.1) 상권정보 변수 추가
    trading_area_data = pd.read_csv("/home/seho/Passenger_Demand/data/울산광역시_상권정보_201231.csv")
    # 상권 정보 전처리
    trading_area_data = preprocessing_trading_area_data(trading_area_data = trading_area_data)
    trading_area_category_list = trading_area_data["category"].drop_duplicates().to_list()
    bus_stop_info = parallelize_dataframe(df = bus_stop_info, 
                                        func = count_nearby, 
                                        num_cores = num_cores, 
                                        col_nm = "trading_area",
                                        nearby_data = trading_area_data, 
                                        dist = 0.2,
                                        category_list = trading_area_category_list)

    # 4.2) 병원벙보 변수 추가
    hospital_data = pd.read_csv("/home/seho/Passenger_Demand/data/api_data/hospital_data.csv")
    # 병원 정보 전처리
    hospital_data = preprocessing_hospital_data(hospital_data = hospital_data)
    hospital_category_list = hospital_data["category"].drop_duplicates().to_list()
    bus_stop_info = parallelize_dataframe(df = bus_stop_info, 
                                        func = count_nearby, 
                                        num_cores = num_cores, 
                                        col_nm = "hospital",
                                        nearby_data = hospital_data, 
                                        dist = 0.2,
                                        category_list = hospital_category_list)


    # 4.3) 학교정보 변수 추가
    school_data = pd.read_csv("/home/seho/Passenger_Demand/data/school_data.csv")
    # 학교 정보 전처리
    school_data = preprocessing_school_data(school_data = school_data)

    school_category_list = school_data["category"].drop_duplicates().to_list()
    bus_stop_info = parallelize_dataframe(df = bus_stop_info, 
                                        func = count_nearby, 
                                        num_cores = num_cores,
                                        col_nm = "school",
                                        nearby_data = school_data, 
                                        dist = 0.2,
                                        category_list = school_category_list)


    all_date = pd.merge(all_date, bus_stop_info.drop(["stop_nm", "latitude", "longitude"], 1), on = ["stop_id"])

    print(f"Finished ({all_date.shape})")

    ######## 5. 시공간적 특성 정보 추가 (행사정보, 축제정보) ########
    print("5. 시공간적 특성 정보 추가 (행사정보, 축제정보) ... ")
    # 5.1 ) 행사 정보 변수 추가
    event_data = pd.read_csv("~/Passenger_Demand/data/event_data.csv")
    event_data = preprocess_event_data(event_data = event_data, start_date = "2020-01-01", end_date = "2020-12-31")
    all_date = parallelize_dataframe(df = all_date, 
                                     func = count_time_nearby, 
                                     num_cores = 12, 
                                     date_col = "transdate",
                                     col_nm = "event",
                                     nearby_data = event_data, 
                                     dist = 0.2)


    # 5.2) 
    festival_data = pd.read_csv("~/Passenger_Demand/data/festival_data.csv")
    festival_data = preprocess_festival_data(festival_data = festival_data, start_date = "2020-01-01", end_date = "2020-12-31")
    all_date = parallelize_dataframe(df = all_date, 
                                    func = count_time_nearby, 
                                    num_cores = 12, 
                                    date_col = "transdate",
                                    col_nm = "event",
                                    nearby_data = event_data, 
                                    dist = 0.2)

    print(f"Finished ({all_date.shape})")



    return all_date
def create_lag_feature(data, 
                       target_cols, 
                       date_cols, 
                       lags, 
                       groupby_cols = None):
    """
        lag feature를 생성
        
        Args: 
            data: 데이터 (Pandas.DataFrame)
            target_cols: 적용 대상 컬럼명 (list, str)
            date_col: 날짜 컬럼명 (str)
            lags: Lag 단위 (list, str)
            groupby_cols: groupby를 수행하는 키 컬럼명 (list, str)

        Returns: 
            data: lag feature를 생성한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """    
    data = data.copy()
    
    # str, list 모두 받을 수 있게 처리
    # -> list가 아닌 경우, 이를 list(str)로 변환
    if isinstance(lags, list) == False:
        lags = [lags]
    if isinstance(date_cols, list) == False:
        date_cols = [date_cols]
    if isinstance(target_cols, list) == False:
        target_cols = [target_cols]
    if isinstance(groupby_cols, list) == False:
        groupby_cols = [groupby_cols]
                
    # 여러 Lag에 대한 변수들을 생성
    # lag 변수를 생성하여 data에 left join하여 변수 추가
    for lg in lags:
        if groupby_cols is None:
            cnt_bf = data.set_index(date_cols)[target_cols].shift(freq = lg).reset_index()
        else:
            cnt_bf = data.set_index(date_cols).groupby(groupby_cols)[target_cols].shift(freq = lg).reset_index()
        
        rename_dict = {col: f"{col}_bf_{lg}" for col in target_cols}
        cnt_bf = cnt_bf.rename(columns = rename_dict)
        
        data = pd.merge(data, cnt_bf, on = date_cols + groupby_cols, how = "left")
    
    return data



def calculate_moving_agg(data, 
                         target_cols, 
                         date_col, 
                         groupby_cols, 
                         col_nm = "", 
                         rollings = ["2d"], 
                         agg_func = [np.mean, np.std]):
    """
        이동집계(평균, 표준편차)를 산출
        
        Args: 
            data: 데이터 (Pandas.DataFrame)
            target_cols: 적용 대상 컬럼명 (list, str)
            date_col: 날짜 컬럼명 (str)
            groupby_cols: groupby를 수행하는 키 컬럼명 (list, str)
            col_nm: 결과 컬럼명 (str)
            rollings: rolling을 수행하는 단위 (list, str)
            agg_fucn: 집계 함수 (list, func)

        Returns: 
            data: 이동집계(평균, 표준편차)를 산출한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    
    # str, list 모두 받을 수 있게 처리
    # -> list가 아닌 경우, 이를 list(str)로 변환    
    if isinstance(target_cols, list) == False:
        target_cols = [target_cols]
        
    if isinstance(groupby_cols, list) == False:
        groupby_cols = [groupby_cols]
        
    if col_nm != "":
        col_nm = f"{col_nm}_"
    
    
    for rl in rollings:
        for tg in target_cols:
            data = data.set_index(date_col).sort_index(ascending=True).copy()
            rolling_data = data.groupby(groupby_cols)[tg].rolling(rl).agg(agg_func)
            rolling_data = rolling_data.rename(columns = {"mean" : f"{tg}_ma_{col_nm}mean_{rl}", 
                                                          "std" : f"{tg}_ma_{col_nm}std_{rl}"})
            rolling_data = rolling_data.groupby(groupby_cols).shift(1).reset_index()    
            
            data = pd.merge(data.reset_index(), rolling_data, on = [date_col] + groupby_cols, how = "left")
            
    return data
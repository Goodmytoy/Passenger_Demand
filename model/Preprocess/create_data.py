import pandas as pd
import numpy as np

def create_data_agg(data, 
                    date_col, 
                    stop_id_col, 
                    target_cols, 
                    freq = None, 
                    groupby_cols = None, 
                    agg_dict = None, 
                    agg_func = sum):
    """
        데이터를 시간, 정류장에 따라 Groupby Aggregation을 수행

        Args: 
            data: 데이터 (Pandas.DataFrame)
            date_col: 날짜 컬럼명 (str)
            stop_id_col: 정류장 컬럼명 (str)
            target_cols: 집계 대상 컬럼 명 (list, str)
            freq: 집계할 날짜 단위 (str)
            groupby_cols: groupby를 수행하는 추가 키 (list, str)
            agg_dict: 대상 컬럼들별로 어떤 집계 방법을 사용하는지에 대한 Dictionary (dict)
                      (값이 입력되면 agg_func는 무시된다.)
            agg_func: 대상 컬럼들에 사용할 집계 함수 (func)

        Returns: 
            data_agg: 집계된 데이터 프레임 (Pandas.DataFrame)

        Exception: 
            
    """
    # str, list 모두 받을 수 있게 처리
    # -> list가 아닌 경우, 이를 list(str)로 변환
    if isinstance(target_cols, list) == False:
        target_cols = [target_cols]
        
    if isinstance(groupby_cols, list) == False:
        if groupby_cols is None:
            groupby_cols = []
        else:
            groupby_cols = [groupby_cols]
    
    grouper = pd.Grouper(key = date_col, freq = freq)
    
    if agg_dict is None:
        agg_dict = {col : agg_func for col in target_cols}
    
    groupby_cols.append(stop_id_col)
    if freq is not None:
        groupby_cols.append(grouper)

    data_agg = (data.groupby(groupby_cols)
                    .agg(agg_dict)
                    .reset_index())
    
    return data_agg



def add_time_features(data, 
                      date_col):
    """
        시간 변수들을 추가 (요일, 시간, 일자, 월, 주)

        Args: 
            data: 데이터 (Pandas.DataFrame)
            date_col: 날짜 컬럼명 (str)

        Returns: 
            data: 시간 변수들을 추가한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    
    # 시간 변수들 생성
    # 요일
    data["dayofweek"] = data[date_col].dt.dayofweek
    dow_dict = {0:"월", 1:"화", 2:"수", 3:"목", 4:"금", 5:"토", 6:"일"}
    data["dayofweek"] = data["dayofweek"].replace(dow_dict)
    # 시간
    data["hour"] = data[date_col].dt.hour
    # 일
    data["date"] = data["transdate"].dt.date   
    # 월
    data["month"] = data[date_col].dt.month
    # 주
    data["weekofyear"] = data[date_col].dt.weekofyear()

    data["hour"] = data["hour"].astype(str)
    data["month"] = data["month"].astype(str)
    data["weekofyear"] = data["weekofyear"].astype(str)
  
    return data




def create_all_date(data, 
                    date_col, 
                    stop_id_col, 
                    except_hours = None):
    """
        모든 시간대의 값을 채워 넣은 데이터 생성

        Args: 
            data: 데이터 (Pandas.DataFrame)
            date_col: 날짜 컬럼명 (str)
            stop_id_col: 정류장 컬럼명 (str)
            except_hours: 제외할 시간대 (list, str)

        Returns: 
            all_date: 모든 시간대의 값을 채워 넣은 데이터 (Pandas.DataFrame)

        Exception: 
            
    """
    # str, list 모두 받을 수 있게 처리
    # -> list가 아닌 경우, 이를 list(str)로 변환
    if isinstance(except_hours, list) == False:
        except_hours = [except_hours]
        
    # 정류장별 모든 시간대의 조합을 생성해 버스 집계 데이터를 Join
    # 데이터가 존재하지 않는 시간대 : NA -> 이후 Impute
    
    # 데이터의 시작과 끝 사이를 1시간 간격으로 구분하여 list 생성
    dt_list = pd.date_range(start = data[date_col].min(), end = data[date_col].max(), freq = "1h")
    date_df = pd.DataFrame({date_col : dt_list}).reset_index(drop = True)
    stop_id_df = pd.DataFrame({stop_id_col : data[stop_id_col].drop_duplicates()}).reset_index(drop = True)

    # 전체 일정(시간 단위)과 정류소 별 조합 DF 생성
    all_date = pd.merge(date_df, stop_id_df, how = "cross")
    
    
    
    # 결측일의 데이터를 채워넣은 전체 데이터를 left join
    all_date = pd.merge(all_date, data.drop(["stop_nm", "longitude", "latitude"], 1), on = [date_col, stop_id_col], how = "left")
    
    # 정류장 정보 추가
    bus_stop_info = data[["stop_id", "stop_nm", "longitude", "latitude"]].drop_duplicates()
    all_date = pd.merge(all_date, bus_stop_info, on = stop_id_col, how = "inner")
    
    # 운행하지 않는 시간대 제외
    all_date = all_date.loc[all_date[date_col].dt.hour.isin(except_hours) == False]
    
    return all_date
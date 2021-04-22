import pandas as pd
import numpy as np

def find_seq_y(data, 
               criterion = 3):
    """
        Y/N 중에 일정 횟수 이상 연속된 Y의 수를 체크하는 함수
        e.g.) 기준 : 3일
        (Y,Y,Y,N,N,Y,Y,N,N,Y,Y) -> (3,3,3,0,0,0,0,0,0,0,0)
        
        Args: 
            data: Y/N 리스트 (list, Pandas Series)
            criterion: 날짜 컬럼명 (str)

        Returns: 
            data: lag feature를 생성한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """    
    seq_list = []
    Y_cnt = 0
    for i, x in enumerate(data):
        # Y인 동안은 Y의 개수를 누적
        if x == "Y":
            Y_cnt += 1
        # N이 등장하거나, 데이터의 끝에 도달한 경우, 
        # 
        if (x == "N") | (i == len(data)):
            if Y_cnt >= criterion:
                temp_list = ["Y"] * Y_cnt
                seq_list += temp_list
            elif (Y_cnt > 0) & (Y_cnt < criterion):
                temp_list = ["N"] * Y_cnt
                seq_list += temp_list
            seq_list.append("N")
            Y_cnt = 0
            
    return seq_list


def preprocess_holiday_data(holiday_data, 
                            date_col = "locdate"):
    """
        특일 데이터를 전처리 하는 함수
        
        Args: 
            holiday_data: 특일 데이터 (Pandas.DataFrame)
            date_col: 날짜 컬럼명 (str)

        Returns: 
            data: lag feature를 생성한 데이터 (Pandas.DataFrame)

        Exception: 
            
    """    
    holiday_data["date"] = pd.to_datetime(holiday_data[date_col], format = "%Y%m%d")
    
    # 전체 일자 생성
    start_year = holiday_data["date"].dt.year.min()
    end_year = holiday_data["date"].dt.year.max()
    
    date_df = pd.DataFrame({"date" : pd.date_range(f"{start_year}-01-01", f"{end_year}-12-31", freq = "1D")})
    
    # 1) 주말 여부
    # 주말 여부를 Y/N으로 표시
    date_df["weekend"] = np.where(date_df["date"].dt.dayofweek.isin([5,6]), "Y", "N")    
    
    # 2) 공휴일, 명절 여부
    # 명절(ntl_holiday)
    ntl_holiday = holiday_data.loc[holiday_data["dateName"].isin(["설날", "추석"])]
    ntl_holiday = ntl_holiday.rename(columns = {"dateName" : "ntl_holi"})
    # 공휴일(holiday) 
    holiday = holiday_data.loc[holiday_data["dateName"].isin(["설날", "추석"]) == False]
    holiday = holiday.rename(columns = {"dateName" : "holi"})
    
    # 곻휴일, 명절 여부 추가 (left join)
    date_df = pd.merge(date_df, ntl_holiday.drop("locdate", 1), on = "date", how = "left")
    date_df = pd.merge(date_df, holiday.drop("locdate", 1), on = "date", how = "left")
    date_df["ntl_holi"] = np.where(date_df["ntl_holi"].isna(),"N", "Y")
    date_df["holi"] = np.where(date_df["holi"].isna(),"N", "Y")
    
    # 3) 3일 이상 연휴 여부
    date_df["rest_yn"] = date_df[["weekend", "ntl_holi", "holi"]].apply(lambda x: any(x == "Y"), 1)
    date_df["rest_yn"] = np.where(date_df["rest_yn"],"Y", "N")
    
    # 3번 이상 연속된 휴일 찾기
    date_df["seq_holi"] = find_seq_y(data = date_df["rest_yn"], criterion = 3)
    date_df = date_df.drop(["weekend", "rest_yn"], 1)
    date_df["date"] = date_df["date"].dt.date
    
    return date_df
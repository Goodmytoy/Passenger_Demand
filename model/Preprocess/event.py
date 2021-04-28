import pandas as pd
import numpy as np

def preprocess_event_data(event_data, 
                          start_date, 
                          end_date):
    """
        행사 데이터 전처리 함수

        Args: 
            event_data: 행사 데이터 (Pandas.DataFrame)
            start_date: 시작 일자 (str)
            end_date: 종료 일자 (str)

        Returns: 
            event_data: 행사 데이터 (Pandas.DataFrame)

        Exception: 
    """
    # 날짜 컬럼으로 변환
    event_data["eventStartDate"] = pd.to_datetime(event_data["eventStartDate"])
    event_data["eventEndDate"] = pd.to_datetime(event_data["eventEndDate"])
    
    # 시간 컬럼 정제
    event_data["eventStartTime"] = (event_data["eventStartTime"].str.extract(r"(\d+):")[0]
                                                                .str.pad(width=2, side='left', fillchar='0')
                                                                .replace({"24":"23"}))
    event_data["eventEndTime"] = (event_data["eventEndTime"].str.extract(r"(\d+):")[0]
                                                            .str.pad(width=2, side='left', fillchar='0')
                                                            .replace({"24":"23"}))
    
    # 날짜와 시간 컬럼을 붙여 datetime으로 변환
    event_data["startDate"] = pd.to_datetime(event_data["eventStartDate"].dt.strftime("%Y-%m-%d") + " " + event_data["eventStartTime"], format = "%Y-%m-%d %H")
    event_data["endDate"] = pd.to_datetime(event_data["eventEndDate"].dt.strftime("%Y-%m-%d") + " " + event_data["eventEndTime"], format = "%Y-%m-%d %H")
    
    # 필요한 컬럼 추출
    event_data = event_data[["eventNm", "rdnmadr", "startDate", "endDate", "latitude", "longitude"]]
    # (start_date, end_date) 범위 사이의 데이터만 추출
    event_data = event_data.loc[event_data["startDate"].dt.date.between(pd.to_datetime(start_date).date(), 
                                                                        pd.to_datetime(end_date).date())].reset_index(drop = True)
    
    # 위/경도 좌표 Float 형식으로 변환
    # (str인 경우 havesine에서 에러 발생)
    event_data["longitude"] = event_data["longitude"].astype(float)
    event_data["latitude"] = event_data["latitude"].astype(float)

    return event_data
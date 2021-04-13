##########################################
# 행사 데이터 수집
##########################################
from utils.Event_Data_by_API import * 
import os
    
def Load_Event_Data(params_dict,
                    start_year = '',
                    select_region = '', 
                    save_tf = False, 
                    save_path = os.getcwd()):
    
    event_api = Event_Data_by_API(params_dict = params_dict)
    event_data = event_api.get()
    
    # 날짜데이터 형변환
    event_data["eventStartDate"] = pd.to_datetime(event_data["eventStartDate"], format = "%Y-%m-%d")
    event_data["eventEndDate"] = pd.to_datetime(event_data["eventEndDate"], format = "%Y-%m-%d")
    event_data["referenceDate"] = pd.to_datetime(event_data["referenceDate"], format = "%Y-%m-%d")

    # 선택된 지역 데이터 추출
    if select_region != '':
        event_data = event_data.loc[event_data["rdnmadr"].str.contains(select_region)]
        
    # 시작연도 데이터 추출
    if start_year != '':
        event_data = event_data.loc[(event_data["eventStartDate"].dt.year == start_year)]
    
    # index 초기화
    event_data = event_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        event_data.to_csv(save_path +'/event_data.csv', index=False)
    else :
        return event_data

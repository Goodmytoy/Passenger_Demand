##########################################
# 축제 데이터 수집
##########################################
from utils.Festival_Data_by_API import * 
import os
    
def Load_Festival_Data(params_dict, 
                       start_year = '',
                       select_region = '', 
                       save_tf = False, 
                       save_path = os.getcwd()):
    
    festival_api = Festival_Data_by_API(params_dict = params_dict)
    festival_data = festival_api.get()
    
    # 날짜데이터 형변환
    festival_data["fstvlStartDate"] = pd.to_datetime(festival_data["fstvlStartDate"], format = "%Y-%m-%d")
    festival_data["fstvlEndDate"] = pd.to_datetime(festival_data["fstvlEndDate"], format = "%Y-%m-%d")
    festival_data["referenceDate"] = pd.to_datetime(festival_data["referenceDate"], format = "%Y-%m-%d")

    # 선택된 지역 데이터 추출
    if select_region != '':
        festival_data = festival_data.loc[festival_data["rdnmadr"].str.contains(select_region)]
        
    # 시작연도 데이터 추출
    if start_year != '':
        festival_data = festival_data.loc[(festival_data["fstvlStartDate"].dt.year == start_year)]
    
    # index 초기화
    festival_data = festival_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        festival_data.to_csv(save_path +'/festival_data.csv', index=False)
    else :
        return festival_data

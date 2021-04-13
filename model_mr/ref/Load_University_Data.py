##########################################
# 대학 데이터 수집
##########################################
from utils.University_Data_by_API import *
from utils.Geocoding_by_API import *
import os
    
def Load_University_Data(params_dict,
                         google_key,
                         select_region = '', 
                         save_tf = False, 
                         save_path = os.getcwd()):
    
    university_api = University_Data_by_API(params_dict = params_dict)
    university_data = university_api.get()
    
    # 선택된 지역 데이터 추출
    if select_region != '':
        university_data = university_data.loc[university_data["region"].str.contains(select_region)]

    # Geocoding
    university_data = get_geocodeDf(university_data, "adres", google_key)
    
    # index 초기화
    university_data = university_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        university_data.to_csv(save_path +'/university_data.csv', index=False)
    else :
        return university_data

from utils.Particulate_Matter_Data_by_API import *
import os

def Load_Particulate_Matter_Data(params_dict,
                                 save_tf = False, 
                                 save_path = os.getcwd()):
    
    pm_api = PM_Data_by_API(params_dict = params_dict)
    pm_data = pm_api.get()
    
    # index 초기화
    pm_data = pm_data.reset_index(drop=True)
  
    # 저장여부 변수가 True면 csv파일로 저장, False면 Df로 리턴
    if save_tf == True :
        pm_data.to_csv(save_path +'/pm_data.csv', index=False)
    else :
        return pm_data
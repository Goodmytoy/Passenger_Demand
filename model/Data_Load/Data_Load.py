import Data_Load
import pandas as pd
import numpy as np


class Data_API:
    def __init__(self, service_key, google_key):
        self.service_key = service_key
        self.google_key = google_key

    
    def get(self, city, base_year, params_dict, save_path = None):
        self.save_path = save_path

        if save_path is not None:
            save_tf = True
        else:
            save_tf = False
        
        # 휴일 정보 수집
        print("휴일 정보 수집 ... " , end = "")
        self.holiday_data = Data_Load.Load_Holiday_Data(params_dict["holiday"], 
                                                        save_tf = save_tf, 
                                                        save_path = save_path)
        print("완료")

        # 날씨 정보 수집
        print("날씨 정보 수집 ... " , end = "")
        self.weather_data = Data_Load.Load_Weather_Data(params_dict["weather"], 
                                                        save_tf = save_tf, 
                                                        save_path = save_path)
        print("완료")

        # 미세먼지 경보 정보 수집
        print("미세먼지 경보 정보 수집 ... " , end = "")
        self.pm_data = Data_Load.Load_Particulate_Matter_Data(params_dict["pm"], 
                                                                save_tf = save_tf, 
                                                                save_path = save_path)
        print("완료")

        # 상권 정보 수집
        print("상권 정보 수집 ... " , end = "")
        self.trading_area_data = Data_Load.Load_Trading_Data(params_dict["trading_area"],
                                                             google_key = self.google_key,
                                                             select_region = city,
                                                             save_tf = save_tf, 
                                                             save_path = save_path)
        print("완료")

        # 병원 정보 수집
        print("병원 정보 수집 ... " , end = "")
        self.hospital_data = Data_Load.Load_Hospital_Data(params_dict["hospital"], 
                                                          save_tf = save_tf, 
                                                          save_path = save_path)
        print("완료")

        # 학교(초중고) 정보 수집
        print("학교(초중고) 정보 수집 ... " , end = "")
        self.school_data = Data_Load.Load_School_Data(params_dict["school"], 
                                                      select_region = city, 
                                                      save_tf = save_tf, 
                                                      save_path = save_path)
        print("완료")

        # 대학교 정보 수집
        print("대학교 정보 수집 ... " , end = "")
        self.university_data = Data_Load.Load_University_Data(params_dict["university"],
                                                              google_key = self.google_key,
                                                              select_region = city,
                                                              save_tf = save_tf, 
                                                              save_path = save_path)
        print("완료")

        # 행사 정보 수집
        print("행사 정보 수집 ... " , end = "")
        self.event_data = Data_Load.Load_Event_Data(params_dict["event"],
                                                    start_year = base_year,
                                                    select_region = city,
                                                    save_tf = save_tf,
                                                    save_path = save_path)
        print("완료")

        # 축제 정보 수집
        print("축제 정보 수집 ... " , end = "")
        self.festival_data = Load_Festival_Data(params_dict["festival"],
                                                start_year = base_year,
                                                select_region = city,
                                                save_tf = save_tf,
                                                save_path = save_path)
        print("완료")

    
    def read(self):
        # 휴일 정보 Load
        self.holiday_data = pd.read_csv(self.save_path + "/holiday_data.csv")
        # 날씨 정보 Load
        self.weather_data = pd.read_csv(self.save_path + "/weather_data.csv")
        # 미세먼지 경보 정보 Load
        self.pm_data = pd.read_csv(self.save_path + "/pm_data.csv")
        # 상권 정보 load
        self.trading_area_data = pd.read_csv(self.save_path + "/trading_data.csv")
        # 병원 정보 Load
        self.hospital_data = pd.read_csv(self.save_path + "/hospital_data.csv")
        # 초중고등학교 정보 Load
        self.school_data = pd.read_csv(self.save_path + "/school_data.csv")
        # 대학교 정보 Load
        self.school_data = pd.read_csv(self.save_path + "/university_data.csv")
        # 행사 정보 Load
        self.event_data = pd.read_csv(self.save_path + "/event_data.csv")
        # 축제 정보 Load
        self.festival_data = pd.read_csv(self.save_path + "/festival_data.csv")
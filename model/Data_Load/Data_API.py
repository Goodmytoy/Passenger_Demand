import Data_Load
import pandas as pd
import numpy as np


class Data_API:
    def __init__(self):
        pass
    
    def get_holiday_data(self, params_dict, save_tf, save_path, year_list):
        """
            휴일 데이터 수집 Method
            (여러 년도의 데이터를 수집할 수 있도록 처리)

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)
                year_list: 년도 리스트 (list)

            Returns: 
                holiday_data: 휴일 데이터 (Pandas.DataFrame)

            Exception: 
        """
        # 휴일 정보 수집
        print("휴일 정보 수집 ... " , end = "")
        holiday_data_list = []
        for yr in year_list:
            params_dict["holiday"]["solYear"] = str(yr)
            holiday_data_list.append(Data_Load.Load_Holiday_Data(params_dict["holiday"], 
                                                                 save_tf = save_tf, 
                                                                 save_path = save_path))
        holiday_data = pd.concat(holiday_data_list, 0)
        print("완료")
        return holiday_data


    def get_weather_data(self, params_dict, save_tf, save_path):
        """
            날씨 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                weather_data: 날씨 데이터 (Pandas.DataFrame)

            Exception: 
        """
        # 날씨 정보 수집
        print("날씨 정보 수집 ... " , end = "")
        weather_data = Data_Load.Load_Weather_Data(params_dict["weather"], 
                                                   save_tf = save_tf, 
                                                   save_path = save_path)
        print("완료")
        return weather_data


    def get_pm_data(self, params_dict, save_tf, save_path, year_list):
        """
            미세먼지 경보 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)
                year_list: 년도 리스트 (list)

            Returns: 
                pm_data: 미세먼지 경보 데이터 (Pandas.DataFrame)

            Exception: 
        """        
        # 미세먼지 경보 정보 수집
        print("미세먼지 경보 정보 수집 ... " , end = "")
        pm_data_list = []
        for yr in year_list:
            params_dict["pm"]["year"] = str(yr)
            pm_data_list.append(Data_Load.Load_Particulate_Matter_Data(params_dict["pm"], 
                                                                       save_tf = save_tf, 
                                                                       save_path = save_path))
            
        pm_data = pd.concat(pm_data_list, 0)
        print("완료")
        return pm_data


    def get_trading_area_data(self, params_dict, city, save_tf, save_path):
        """
            상권 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                trading_area_data: 상권 데이터 (Pandas.DataFrame)

            Exception: 
        """ 
        # 상권 정보 수집
        print("상권 정보 수집 ... " , end = "")
        trading_area_data = Data_Load.Load_Trading_Area_Data(params_dict["trading_area"],
#                                                              google_key = params_dict["google_key"],
#                                                              select_region = city,
                                                             save_tf = save_tf, 
                                                             save_path = save_path)
        print("완료")
        return trading_area_data


    def get_hospital_data(self, params_dict, save_tf, save_path):
        """
            병원 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                hospital_data: 병원 데이터 (Pandas.DataFrame)

            Exception: 
        """         
        # 병원 정보 수집
        print("병원 정보 수집 ... " , end = "")
        hospital_data = Data_Load.Load_Hospital_Data(params_dict["hospital"], 
                                                     save_tf = save_tf, 
                                                     save_path = save_path)
        print("완료")
        return hospital_data


    def get_school_data(self, params_dict, city, save_tf, save_path):
        """
            학교(초중고) 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                school_data: 학교(초중고) 데이터 (Pandas.DataFrame)

            Exception: 
        """         
        # 학교(초중고) 정보 수집
        print("학교(초중고) 정보 수집 ... " , end = "")
        school_data = Data_Load.Load_School_Data(params_dict["school"], 
                                                 select_region = city, 
                                                 save_tf = save_tf, 
                                                 save_path = save_path)
        print("완료")
        return school_data


    def get_university_data(self, params_dict, city, save_tf, save_path):
        """
            대학교 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                university_data: 대학교 데이터 (Pandas.DataFrame)

            Exception: 
        """             
        # 대학교 정보 수집
        print("대학교 정보 수집 ... " , end = "")
        university_data = Data_Load.Load_University_Data(params_dict["university"],
                                                         google_key = params_dict["google_key"],
                                                         select_region = city,
                                                         save_tf = save_tf, 
                                                         save_path = save_path)
        print("완료")
        return university_data


    def get_event_data(self, params_dict, city, save_tf, save_path):
        """
            행사 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                event_data: 행사 데이터 (Pandas.DataFrame)

            Exception: 
        """           
        # 행사 정보 수집
        print("행사 정보 수집 ... " , end = "")
        event_data = Data_Load.Load_Event_Data(params_dict["event"],
                                               start_year = params_dict["start_year"],
                                               end_year = params_dict["end_year"], 
                                               select_region = city,
                                               save_tf = save_tf,
                                               save_path = save_path)
        print("완료")
        return event_data


    def get_festival_data(self, params_dict, city, save_tf, save_path):
        """
            축제 데이터 수집 Method

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_tf: 결과 저장 여부 (Bool)
                save_path: 결과 저장 경로 (str)

            Returns: 
                festival_data: 축제 데이터 (Pandas.DataFrame)

            Exception: 
        """
        # 축제 정보 수집
        print("축제 정보 수집 ... " , end = "")
        festival_data = Data_Load.Load_Festival_Data(params_dict["festival"],
                                                     start_year = params_dict["start_year"],
                                                     end_year = params_dict["end_year"], 
                                                     select_region = city,
                                                     save_tf = save_tf,
                                                     save_path = save_path)
        print("완료")
        return festival_data
    
    
    def get(self, params_dict, city, save_path = None):
        """
            외부 데이터 수집 Method
            (휴일, 날씨, 미세먼지 경보, 상권, 병원, 학교(초중고), 대학교, 행사, 축제)

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)
                city: 도시명 (str)
                save_path: 결과 저장 경로 (str)

            Returns: 

            Exception: 
        """
        self.save_path = save_path
        year_list = range(int(params_dict["start_year"]), int(params_dict["end_year"]) + 1)
        if save_path is not None:
            save_tf = True
        else:
            save_tf = False
        
        self.holiday_data = self.get_holiday_data(params_dict = params_dict, 
                                                  save_tf = save_tf, 
                                                  save_path = save_path, 
                                                  year_list = year_list)
        
        self.weather_data = self.get_weather_data(params_dict = params_dict, 
                                                  save_tf = save_tf, 
                                                  save_path = save_path)
            
        self.pm_data = self.get_pm_data(params_dict = params_dict,
                                        save_tf = save_tf,
                                        save_path = save_path, 
                                        year_list = year_list)
        
        self.trading_area_data = self.get_trading_area_data(params_dict = params_dict,
                                                            city = city, 
                                                            save_tf = save_tf, 
                                                            save_path = save_path)

        self.hospital_data = self.get_hospital_data(params_dict = params_dict, 
                                                    save_tf = save_tf, 
                                                    save_path = save_path)

        self.school_data = self.get_school_data(params_dict = params_dict, 
                                                city = city, 
                                                save_tf = save_tf, 
                                                save_path = save_path)

        self.university_data = self.get_university_data(params_dict = params_dict, 
                                                        city = city, 
                                                        save_tf = save_tf, 
                                                        save_path = save_path)

        self.event_data = self.get_event_data(params_dict = params_dict, 
                                              city = city, 
                                              save_tf = save_tf,
                                              save_path = save_path)

        self.festival_data = self.get_festival_data(params_dict = params_dict,
                                                    city = city, 
                                                    save_tf = save_tf, 
                                                    save_path = save_path)
    
    def read(self):
        """
            외부 데이터를 수집하여 csv 파일로 저장한 경우 이를 다시 불러오는 Method
            (휴일, 날씨, 미세먼지 경보, 상권, 병원, 학교(초중고), 대학교, 행사, 축제)

            Args: 

            Returns: 

            Exception: 
        """
        # 휴일 정보 Load
        self.holiday_data = pd.read_csv(self.save_path + "/holiday_data.csv")
        # 날씨 정보 Load
        self.weather_data = pd.read_csv(self.save_path + "/weather_data.csv")
        # 미세먼지 경보 정보 Load
        self.pm_data = pd.read_csv(self.save_path + "/pm_data.csv")
        # 상권 정보 load
        self.trading_area_data = pd.read_csv(self.save_path + "/trading_area_data.csv")
        # 병원 정보 Load
        self.hospital_data = pd.read_csv(self.save_path + "/hospital_data.csv")
        # 초중고등학교 정보 Load
        self.school_data = pd.read_csv(self.save_path + "/school_data.csv")
        # 대학교 정보 Load
        self.university_data = pd.read_csv(self.save_path + "/university_data.csv")
        # 행사 정보 Load
        self.event_data = pd.read_csv(self.save_path + "/event_data.csv")
        # 축제 정보 Load
        self.festival_data = pd.read_csv(self.save_path + "/festival_data.csv")
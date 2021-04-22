# service_key = 'eLWdQyzctRdtv8bEOuewsTtK6sNkoWp1bE74OUBk43jg4tU6AsI6yYt6Z%2B7sOeaqtB5pTH2yHuPRIuEHtu5amQ%3D%3D'
# google_key = "ReOsv=IfT43PVLSiA4vDRjs=40TCqIw97oVP2D9QpmU="

service_key = 'eLWdQyzctRdtv8bEOuewsTtK6sNkoWp1bE74OUBk43jg4tU6AsI6yYt6Z%2B7sOeaqtB5pTH2yHuPRIuEHtu5amQ%3D%3D'
career_net_key = "24b216ad9062d687e0745d2d847255bc"
google_key = "AIzaSyDfLv3OzniRbUc7tTRBJndpiuyepHSmUrE"

class parameters:
    def __init__(self, service_key, google_key, career_net_key, city, start_year, end_year):
        self.service_key = service_key
        self.google_key = google_key
        self.career_net_key = career_net_key
        self.city = city,
        self.start_year = start_year
        self.end_year = end_year
    
    def _create_holiday_params(self):
        self.holiday_params = {"serviceKey" : self.service_key,
                               "solYear" : self.start_year}

    def _create_weather_params(self):
        self.weather_params = {"serviceKey" : self.service_key,
                               "stnIds" : "152",
                               "startDt" : f"{self.start_year}0101",
                               "startHh" : "00",
                               "endDt" : f"{self.end_year}1231", 
                               "endHh" : "23",
                               "numOfRows" : "900",
                               "dataType" : "JSON",
                               "pageNo" : "1",
                               "dataCd" : "ASOS",
                               "dateCd" : "HR"}

    def _create_pm_params(self):
        self.pm_params = {"serviceKey" : self.service_key,
                          "returnType" : "json",
                          "numOfRows" : 1000,
                          "pageNo" : 1,
                          "year" : self.start_year}

    def _create_trading_area_params(self):
        self.trading_area_params = {"serviceKey" : self.service_key,
                                    "pageNo" : 1,
                                    "numOfRows" : 100,
                                    "radius" : 10000,
                                    "type" : "json"}

    def _create_hospital_params(self):
        self.hospital_params = {"ServiceKey" : self.service_key,
                                "pageNo" : 2,
                                "numOfRows" : 1000,
                                "sidoCd" : 260000}

    def _create_school_params(self):
        self.school_params = {"serviceKey" : self.service_key,
                              "pageNo" : 1,
                              "numOfRows" : 1000,
                              "type" : "xml"}

    def _create_university_params(self):
        self.university_params = {"apiKey" : self.career_net_key,
                                  "svcType" : 'api',
                                  "svcCode" : 'SCHOOL',
                                  "gubun" : 'univ_list',
                                  "thisPage" : 1,
                                  "perPage" : 1000,
                                  "contentType" : "json"}
    
    def _create_event_params(self):
        self.event_params = {"serviceKey" : self.service_key,
                             "pageNo" : 1,
                             "numOfRows" : 1000,
                             "type" : "json"}

    def _create_festival_params(self):
        self.festival_params = {"serviceKey" : self.service_key,
                                "pageNo" : 1,
                                "numOfRows" : 1000,
                                "type" : "json"}
    
    def get(self):
        self._create_holiday_params()
        self._create_weather_params()
        self._create_pm_params()
        self._create_trading_area_params()
        self._create_hospital_params()
        self._create_school_params()
        self._create_university_params()
        self._create_event_params()
        self._create_festival_params()

        params_dict = {"holiday" : self.holiday_params,
                       "weather" : self.weather_params,
                       "pm" : self.pm_params,
                       "trading_area" : self.trading_area_params,
                       "hospital" : self.hospital_params,
                       "school" : self.school_params,
                       "university" : self.university_params,
                       "event" : self.event_params,
                       "festival" : self.festival_params,
                       "start_year" : self.start_year,
                       "end_year" : self.end_year,
                       "service_key" : self.service_key,
                       "google_key" : self.google_key,
                       "career_net_key" : self.career_net_key}
        
        return params_dict
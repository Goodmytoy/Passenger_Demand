import requests
import ast
import xmltodict
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict


class Data_by_API(object):
    """
        API를 통해 데이터를 수집하는 Class

    """    
    def __init__(self, url):
        self.url = url
        self.features = None
        self.main_key = None
    
    def calculate_max_page(self, type = "json"):
        """
            최대 Page 수를 찾는 Method
            (한 화면에 보여지는 Row 수(numofRows)에 따라서 전체 Page가 달라질 수 있으므로, 최대 Page를 찾은 후 해당 값만큼 Loop을 수행)

            Args: 
                type: json/xml 여부 (str) 

            Returns: 
                max_page: 최대 페이지 수 (int)

            Exception: 
        """
        rq = self.request()
        
        rq_dict = self.to_dict(txt = rq.text, type = type)
        
        self.n_rows = int(self.params_dict["numOfRows"])
        
        if type == "json":
            self.total_count = int(rq_dict["response"]["body"]["totalCount"])
        elif type == "xml":
            xmlsoup = BeautifulSoup(rq.text,'html.parser')
            self.total_count = int(xmlsoup.find("totalcount").text)
                
        max_page = int(np.ceil(self.total_count / self.n_rows))
        
        print(f"n_rows : {self.n_rows}, total_count : {self.total_count}, max_page = {max_page}")
        
        return max_page
    
    
    def create_request_url(self, params_dict):
        """
            API 요청 파라미터들을 활용해 Request URL 생성

            Args: 
                params_dict: API 요청 파라미터 (Dictionary)

            Returns: 
                request_url: 파라미터들의 값이 포함된 request url (str)

            Exception: 
        """
        params_list = [f"{k}={v}" for k, v in params_dict.items()]
        params_str = "&".join(params_list)
        
        self.request_url = self.url + params_str
        
        return self.request_url
    
    
    def create_request_urls(self):
        """
            max_page까지 조회하는 Request URL들을 list 형태로 생성하는 Method
            (필요에 따라 다른 형태의 request_urls를 만들도록 overriding 하여 사용)

            Args: 

            Returns: 
                request_urls: 조회할 Request url 들의 list (list)

            Exception: 
        """
        max_page = self.calculate_max_page(type = self.type)
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["pageNo"] = i + 1
            request_urls.append(self.create_request_url(params_dict = params_dict))
            
        return request_urls
    

    
    def to_dict(self, txt, type):
        """
            request 결과(json/xml)를 Dictionary 형태로 변환하는 Method

            Args: 
                txt: request 결과 (str)
                type: json/xml (str)

            Returns: 
                rq_dict: request 결과 Dictionary (Dict)

            Exception: 
        """
        # json / xml to dict
        if type == "json":
            rq_dict = ast.literal_eval(txt)
        elif type == "xml":
            rq_dict = xmltodict.parse(txt)
            
        return rq_dict
    
    
    def extract_values_from_dict(self, dct):
        """
            Request Dictionary 로 부터 필요한 item들을 추출하는 Method
            (API마다 다양한 케이스가 있어 필요한 경우, overriding하여 사용)

            Args: 
                dct: request 결과 Dictionary (dict)

            Returns: 
                dict_list: item들의 list (list)

            Exception: 
        """
        try: 
            dict_list = dct["response"]["body"]["items"]["item"]
        except:
            dict_list = dct["response"]["body"]["items"]
            
        return dict_list
    

    def request(self, request_url = None):
        """
            Request URL을 통해 Request 값을 받아오는 Method

            Args: 
                request_url: Request URL (str)

            Returns: 
                rq: request object

            Exception: 
        """
        if request_url == None:
            request_url = self.request_url
            
        rq = requests.get(request_url, allow_redirects = True)
        
        return rq

    
    def parse(self, request, features = None, type = "json"):
        """
            API를 통해 데이터를 Parsing하는 Method

            Args: 
                request: request object
                features: 데이터의 feature list (list)
                type: json/xml (str)

            Returns: 
                data_dict: Parsing한 데이터의 Dictionary (Dictionary)

            Exception: 
        """
        data_dict = defaultdict(list)
        
        rq_dict = self.to_dict(txt = request.text, type = type)
        
        # 일부 url의 경우는 item이 아닌 items에 값이 존재
        dict_list = self.extract_values_from_dict(dct = rq_dict)
        self.dict_list = dict_list
        # 값이 1개인 경우 list가 아니라 dictionary 1개가 반환되므로, 이를 list(dict)형태로 변환
        if isinstance(dict_list, dict):
            dict_list = [dict_list]
        
        # item이 없는 경우 빈 Dictionary(data dict)를 반환
        if dict_list is None:
            return data_dict
        
        if features is None:
            features = dict_list[0].keys()
            
        for x in dict_list:
            for col in features:
                data_dict[col].append(x.get(col))

        return data_dict
    
    
    def get(self):
        """
            데이터를 가져오는 Method

            Args: 

            Returns: 
                API를 통해 가져온 DataFrame (Pandas.DataFrame)

            Exception: 
        """
        self.request_urls = self.create_request_urls()
        
        data_dict = defaultdict(list)
        for request_url in self.request_urls:
            for _ in range(5):
                try:
                    rq = self.request(request_url = request_url)
                    temp_dict = self.parse(request = rq, features = None, type = self.type)
                    break
                except:
                    pass
                
            for k, v in temp_dict.items():
                data_dict[k].extend(v)
            
            del temp_dict
        return pd.DataFrame(data_dict)
        
# -*- coding: utf-8 -*-
import requests
import ast
import xmltodict
import numpy as np
from bs4 import BeautifulSoup
from collections import defaultdict


class Data_by_API(object):
    
    def __init__(self, url):
        self.url = url
        self.features = None
        self.main_key = None
#         self.serviceKey = serviceKey
    
    
    def calculate_max_page(self, type = "json"):
        rq = self.request()
        
        rq_dict = self.to_dict(txt = rq.text, type = type)
        
        self.n_rows = int(self.params_dict["numOfRows"])
        
        try:
            self.total_count = int(rq_dict["response"]["body"]["totalCount"])
        except:
            xmlsoup = BeautifulSoup(rq.text,'html.parser')
            self.total_count = int(xmlsoup.find("totalcount").text)
                
        max_page = int(np.ceil(self.total_count / self.n_rows))
        
        print(f"n_rows : {self.n_rows}, total_count : {self.total_count}, max_page = {max_page}")
        
        return max_page
    
    
    def create_request_url(self, params_dict):
#         params_dict["service_key"] = self.serviceKey
        params_list = [f"{k}={v}" for k, v in params_dict.items()]
        params_str = "&".join(params_list)
#         print(params_str)
        
        self.request_url = self.url + params_str
        
        return self.request_url
    
    
    def create_request_urls(self):
        max_page = self.calculate_max_page(type = self.type)
        
        params_dict = self.params_dict.copy()
        
        request_urls= []
        for i in range(max_page):
            params_dict["pageNo"] = i + 1
            request_urls.append(self.create_request_url(params_dict = params_dict))
            
        return request_urls
    
    
#     def parse_xml(self, request, features = None):
        
#         data_dict = defaultdict(list)
        
#         xmlsoup = BeautifulSoup(request.text,'html.parser')
#         items = xmlsoup.find_all('item')

#         if features is None:
#             features = [x.name for x in items[0].contents]          
        
#         for item in items:
#             for content in item.contents:
#                 if content.name in features:
#                     data_dict[content.name].append(content.text)
        
#         return data_dict
    
    
#     def parse_json(self, request, features = None):
#         data_dict = defaultdict(list)
#         rq_json = ast.literal_eval(request.text)
        
#         if features is None:
#             features = rq_json["response"]["body"]["items"]["item"][0].keys()
        
#         json_list = rq_json["response"]["body"]["items"]["item"]                                                           
#         for js in json_list:
#             for col in features:
#                 data_dict[col].append(js[col])
        
#         return data_dict
    
    def to_dict(self, txt, type):
        # json / xml to dict
        if type == "json":
            rq_dict = ast.literal_eval(txt)
        elif type == "xml":
            rq_dict = xmltodict.parse(txt)

        return rq_dict
    
    
    def extract_values_from_dict(self, dct):
        try: 
            dict_list = dct["response"]["body"]["items"]["item"]
        except:
            dict_list = dct["response"]["body"]["items"]
        
        return dict_list
    
    
    
    def parse(self, request, features = None, type = "json"):
        
        data_dict = defaultdict(list)
        
        rq_dict = self.to_dict(txt = request.text, type = type)
        
        # 일부 url의 경우는 item이 아닌 items에 값이 존재
        dict_list = self.extract_values_from_dict(dct = rq_dict)
#        try: 
#            dict_list = rq_dict["response"]["body"]["items"]["item"]
#        except:
#            dict_list = rq_dict["response"]["body"]["items"]
        
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
    
    
    def request(self, request_url = None):
        
        if request_url == None:
            request_url = self.request_url
            
        rq = requests.get(request_url, allow_redirects = True)
        
        return rq


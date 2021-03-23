import requests

class Data_by_API(object):
    
    def __init__(self, url):
        self.url = url
#         self.serviceKey = serviceKey
        
    def create_request_url(self, params_dict):
#         params_dict["service_key"] = self.serviceKey
        params_list = [f"{k}={v}" for k, v in params_dict.items()]
        params_str = "&".join(params_list)
#         print(params_str)
        
        self.request_url = self.url + params_str
        
        return self.request_url
    
    
    def request(self, request_url = None):
        
        if request_url == None:
            request_url = self.request_url
            
        rq = requests.get(request_url)
        
        return rq
        
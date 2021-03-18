import requests

class Data_by_API(object):
    
    def __init__(self, url, params_dict):
        self.url = url
        self.params_dict = params_dict
        
    def create_request_url(self):
        params_list = [f"{k}={v}" for k, v in self.params_dict.items()]
        params_str = "&".join(params_list)
        
        self.request_url = self.url + params_str
    
    def request(self):
        
        rq = requests.get(self.request_url)
        
        return rq
        
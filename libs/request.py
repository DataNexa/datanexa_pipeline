import requests 
from libs.config import config,Config

conf   = config()
baseu  = conf['api']
header = {
    'session':Config().getAccount('token'),
    'Content-Type':'application/json'
}

class Request:

    code:int 
    body:dict|list

    def __init__(self, code:int, body:dict|list):
        self.code = code 
        self.body = body

def factory(req):
    try:
        json = req.json()
        return Request(json['code'], json['body'])
    except:
        return Request(req.status_code, {})        

def get(route='/'):
    req = requests.get(baseu+route, headers=header)
    return factory(req)
    

def post(route='/', data={}):
    req = requests.post(baseu+route, json=data, headers=header)
    return factory(req)
import json

from libs.cookies import Cookie, CookieManager

class _ConfSingle(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            instance._start()
            cls._instances[cls] = instance

        return cls._instances[cls]
    

class Config(metaclass=_ConfSingle):
    
    _started = False
    _objs:map = {}
    _accounts:map = {}
    _cookie_manager:CookieManager = None

    def _start(self):

        if self._started: return

        self._objs = json.loads(open("./config.json", "r").read())
        self._accounts = json.loads(open("./accounts.json", "r").read())

        cookies:list[Cookie] = []
        for acc in self._accounts['twitter']:
            cookies.append(Cookie(acc['user'], acc['pass'], "twitter"))
        for acc in self._accounts['facebook']:
            cookies.append(Cookie(acc['user'], acc['pass'], "facebook"))
        for acc in self._accounts['instagram']:
            cookies.append(Cookie(acc['user'], acc['pass'], "instagram"))

        self.cookie_manager = CookieManager(cookies)

        self._started = True

    
    def getDict(self):
        return self._objs 
    
    def getAccount(self, key:str):
        return self._accounts[key]
    
    def getCookieManager(self):
        return self.cookie_manager
    

def config():
    return Config().getDict()
import json

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

    def _start(self):

        if self._started: return

        try:
            self._objs = json.loads(open("./config.json", "r").read())
            self._started = True
        except:
            print("Erro ao tentar ler o arquivo './config.json'")

    
    def getDict(self):
        return self._objs 
    

def config():
    return Config().getDict()
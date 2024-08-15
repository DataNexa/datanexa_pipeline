from entidades.Monitoramento import Monitoramento

class Client:

    _id:int
    _slug:str 
    _nome:str
    _monitoramentos:list[Monitoramento]

    def __init__(self, id:int, slug:str, nome:str):
        self._id = id 
        self._slug = slug 
        self._nome = nome

    def setMonitoramentos(self, monitoramentos:list[Monitoramento]):
        self._monitoramentos = monitoramentos

    def getId(self):
        return self._id 
    
    def getSlug(self):
        return self._slug 
    
    def getNome(self):
        return self._nome
    
    def getTotalMonitoramentos(self):
        return len(self._monitoramentos)
    
    def getMonitoramento(self, k):
        return self._monitoramentos[k]
    
    def getMonitoramentoActive(self):
        k = 0
        for monitoramento in self._monitoramentos:
            if monitoramento.getStatus() < 3:
                return [monitoramento, k]
            k += 1


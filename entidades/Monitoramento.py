
class Monitoramento:
    
    _id:int
    _titulo:str 
    _descr:str 
    _alvo:str 
    _task_status:int
    _pesquisa:str
    _task_id:int
    _hashtags:list[str]

    def __init__(self, id:int, titulo:str, pesquisa:str, alvo:str, task_id:int, task_status:int):
        self._id = id 
        self._titulo = titulo 
        self._alvo = alvo
        self._pesquisa = pesquisa
        self._task_status = task_status 
        self._task_id = task_id

    def setHashtags(self, hashtags:list[str]):
        self._hashtags = hashtags

    def setPesquisa(self, pesquisa:str):
        self._pesquisa = pesquisa

    def setStatus(self, status:int):
        self._task_status = status

    def trabalhando(self):
        self._task_status = 2

    def finalizar(self):
        self._task_status = 3

    def getId(self):
        return self._id

    def getAlvo(self):
        return self._alvo

    def getStatus(self):
        return self._task_status
    
    def getPesquisa(self):
        return self._pesquisa
    
    def getHashtags(self):
        return self._hashtags
    
    def getTaskId(self):
        return self._task_id
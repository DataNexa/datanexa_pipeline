
class Monitoramento:
    
    _id:int
    _titulo:str 
    _descr:str 
    _alvo:str 
    _task_status:int
    _task_id:int

    def __init__(self, id:int, titulo:str, alvo:str, task_id:int, task_status:int):
        self._id = id 
        self._titulo = titulo 
        self._alvo = alvo
        self._task_status = task_status 
        self._task_id = task_id

    def trabalhando(self):
        self._task_status = 2

    def finalizar(self):
        self._task_status = 3

    def getStatus(self):
        self._task_status
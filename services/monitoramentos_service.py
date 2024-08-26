from libs.request import get,post
import time
from entidades.Client import Client
from entidades.Monitoramento import Monitoramento

async def getClients() -> list[Client]:
    
    req = get('/monitoramento/info')
    clientsObj = []
    if req.code == 200:    
        clients = req.body
        for client in clients:
            clientsObj.append(Client(
                client['id'],
                client['slug'],
                client['nome']
            ))
    
    return clientsObj


async def getMonitoramentos(client_id:int) -> list[Monitoramento]:

    req = post('/monitoramento/fila_list', {
        "client_id":client_id
    })

    monitoramentos = []
    jsonList       = req.body
    for item in jsonList:
        try:
            monitoramento = Monitoramento(
                    item['monitoramento_id'],
                    item['titulo'],
                    item['pesquisa'],
                    item['alvo'],
                    item['task_id'],
                    item['task_status']
                )
            monitoramento.setHashtags(item['hashtags'].split())
            monitoramentos.append(monitoramento)
        except:
            pass    

    return monitoramentos


async def changeStatusMonitoramento(monitoramento:Monitoramento, status:int):
    
    req = post('/monitoramento/alterarStatusTask', {
        "task_id":monitoramento.getTaskId(),
        "status":status
    })

    if req.code == 200:
        monitoramento.setStatus(status)
        return True
    
    return False
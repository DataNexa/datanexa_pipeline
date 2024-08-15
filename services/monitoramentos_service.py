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
    jsonList = req.body

    for item in jsonList:
        monitoramentos.append(
            Monitoramento(
                item['monitoramento_id'],
                item['titulo'],
                item['alvo'],
                item['task_id'],
                item['task_status']
            )
        )

    return monitoramentos

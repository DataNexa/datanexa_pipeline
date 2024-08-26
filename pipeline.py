
from services.monitoramentos_service import getClients,getMonitoramentos
from entidades.Client import Client
from entidades.Monitoramento import Monitoramento
import signal
import asyncio
import spiders.spider as spider
import libs.config as config

MAX_CONCURRENT_CLIENTES = 1

semaphore  = asyncio.Semaphore(MAX_CONCURRENT_CLIENTES)
parar_loop = asyncio.Event()

config.Config()

async def start():

    def signal_handler(signum, frame):
        print("Sinal recebido, preparando para parar...")
        parar_loop.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    clients = await getClients()
    for client in clients:
        monitoramentos = await getMonitoramentos(client_id=client.getId())
        client.setMonitoramentos(monitoramentos)
    
    while not parar_loop.is_set():
        tarefas_clientes = [processarCliente(client) for client in clients]
        await asyncio.gather(*tarefas_clientes)

    

async def processarMonitoramento(monitoramento:Monitoramento):
    monitoramento.trabalhando()
    await spider.start(monitoramento)
    monitoramento.finalizar()
    


async def processarCliente(client:Client):
    
    async with semaphore: 
        
        monitoramento = client.getMonitoramentoActive()

        if monitoramento == None:
            monitoramentos = await getMonitoramentos(client_id=client.getId())
            client.setMonitoramentos(monitoramentos)
            monitoramento = client.getMonitoramentoActive()

        if monitoramento is not None:
            await processarMonitoramento(monitoramento)

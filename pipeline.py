
from services.monitoramentos_service import getClients,getMonitoramentos
import asyncio

MAX_CONCURRENT_CLIENTES = 3

semaphore  = asyncio.Semaphore(MAX_CONCURRENT_CLIENTES)

async def start():

    clients = await getClients()

    for client in clients:
        monitoramentos = await getMonitoramentos(client_id=client.getId())
        client.setMonitoramentos(monitoramentos)

    
from entidades.Monitoramento import Monitoramento
from services.monitoramentos_service import changeStatusMonitoramento
import spiders.twitter.twitter as twitter
import spiders.instagram.instagram as instagram
import spiders.youtube.youtube as youtube
import spiders.web.web as web
import asyncio 


def transformar_pesquisa(pesquisa:str):
    
    palavras = pesquisa.split()

    pesquisa_final = ""
    for palavra in palavras:
        pesquisa_final += f"\"{palavra.replace('+', ' ')}\" "
    
    return pesquisa_final


async def start(monitoramento:Monitoramento):

    monitoramento.setPesquisa(transformar_pesquisa(monitoramento.getPesquisa()))
    
    await changeStatusMonitoramento(monitoramento, 2)
    await twitter.start(monitoramento)
    await instagram.start(monitoramento)
    await youtube.start(monitoramento)
    await web.start(monitoramento)
    await changeStatusMonitoramento(monitoramento, 3)
    
    await asyncio.sleep(60)
    
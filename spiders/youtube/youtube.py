from entidades.Monitoramento import Monitoramento 
from entidades.Publish import Publish

from libs.navigator import Navigator 
from spiders.youtube.youtube_lib import search,get_list_publish,continuar
from libs.gpt import analise
from services.publish_service import addPublish

async def start(monitoramento:Monitoramento):

    navigator = Navigator("https://www.youtube.com/")
    search(navigator, monitoramento.getPesquisa())

    limit1 = 60
    cin = 1
    lista:list[Publish] = []
    continando = True

    while continando:
        lista += get_list_publish(navigator)
        if cin > limit1: break
        navigator.scrooldown(body=False)
        navigator.sleep(3)
        print(f"cin: {str(cin)}")
        cin += 1
        continando = continuar(navigator)
    
    listaFinal = analise(monitoramento.getId(), lista, monitoramento.getAlvo())
    
    for item in listaFinal:
        await addPublish(item, monitoramento.getId())


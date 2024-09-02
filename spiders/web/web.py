from entidades.Monitoramento import Monitoramento
from libs.navigator import Navigator
from spiders.web.web_lib import search,get_all_publish
from libs.gpt import analise
from services.publish_service import addPublish

async def start(monitoramento:Monitoramento):

    navigator = Navigator("https://www.google.com/")
    navigator.goto("search?q="+monitoramento.getPesquisa())
    navigator.sleep(5)
    page = 0

    search(navigator)
    current  = navigator.getCurrentURL()
    
    while page < 11:
        
        pubs       = get_all_publish(navigator, page, current)
        analisados = analise(monitoramento.getId(), pubs, monitoramento.getAlvo())
        print("analisados: ", str(len(analisados)))
        
        for pub in analisados:
            await addPublish(pub, monitoramento.getId())

        navigator.sleep(1)
        page += 1

    navigator.quit()
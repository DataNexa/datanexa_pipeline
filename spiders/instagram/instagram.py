from entidades.Monitoramento import Monitoramento
from entidades.Publish import Publish
from libs.navigator import Navigator
from libs.config import Config
from spiders.instagram.instagram_lib import login, checkPop, pesquisa, getPublish, next
from services.publish_service import addPublish
from libs.gpt import analise

SLUG_SERVICE = "instagram"


async def save_publishs(pubs:list[Publish], monitoramento_id:int):
    for pub in pubs:
        await addPublish(pub, monitoramento_id)


async def start(monitoramento:Monitoramento):
    
    manager = Config().getCookieManager()
    cookie  = await manager.pegarCookieLivre(SLUG_SERVICE)

    navigator = Navigator("https://www.instagram.com/", cookie=cookie)
    hashtags  = monitoramento.getHashtags()

    login(navigator)
    checkPop(navigator)
    
    for tag in hashtags:

        if not pesquisa(navigator, tag):
            print("intagram.py - A pesquisa não retornou resultados ou não foi possível clicar na primeira publicação")
            continue

        pubs:list[Publish] = []
        max = 30
        ini = 1

        while True:
            pub = getPublish(navigator)
            if pub != False:
                pubs.append(pub)
            ini += 1
            nex = next(navigator) 
            navigator.sleep(2)
            if not nex or ini > max: break

        pubs_analises = analise(monitoramento.getId(), pubs, monitoramento.getAlvo())
        await save_publishs(pubs_analises, monitoramento.getId())

    navigator.saveState()
    await manager.liberarCookie(cookie)
    navigator.quit()

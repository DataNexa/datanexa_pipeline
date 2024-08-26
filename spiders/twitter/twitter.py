from entidades.Monitoramento import Monitoramento
from libs.config import Config
from libs.navigator import Navigator
from spiders.twitter.twitter_lib import login,checkreload,get_all_publish
from libs.gpt import analise
from services.publish_service import addPublish


async def start(monitoramento:Monitoramento):

    manager = Config().getCookieManager()
    cookie  = await manager.pegarCookieLivre("twitter")
    
    navigator = Navigator("https://www.twitter.com/", cookie=cookie)

    login(navigator)

    navigator.goto("search?q="+monitoramento.getPesquisa()+"&src=typed_query")
    navigator.sleep(5)

    max = 5
    c = 1
    dontstop = True
    
    while dontstop:
        
        checkreload(navigator)
        
        publis = get_all_publish(navigator)
        pubs   = analise(monitoramento.getId(), publis, monitoramento.getAlvo())

        for pub in pubs:
            await addPublish(pub, monitoramento.getId())

        dontstop = c < max
        c+=1
        navigator.scrooldown()
        navigator.sleep(5)

    await manager.liberarCookie(cookie)
    navigator.saveState()
    navigator.quit()

    
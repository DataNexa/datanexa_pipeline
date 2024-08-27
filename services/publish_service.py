from entidades.Publish import Publish
from libs.request import post

async def addPublish(publish:Publish, monitoramento_id:int):
    
    if publish is None: return

    req = post('/publicacoes/add', {
        "monitoramento_id":monitoramento_id,
        "titulo":publish.getTitulo(),
        "texto":publish.getText(),
        "avaliacao":publish.getAvaliacao(),
        "link":publish.getLink(),
        "local_pub":publish.getMidiaSlug(),
        "data_pub":publish.getData()
    })

    return req.code == 200

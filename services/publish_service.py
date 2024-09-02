from entidades.Publish import Publish
from libs.request import post
from datetime import datetime
async def addPublish(publish:Publish, monitoramento_id:int):
    
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


async def getPublishByMedia(media:str):

    req = post('/publicacoes/list_by_media', {
        "media":media
    })

    publishs:list[Publish] = []

    for row in req.body:

        pub = Publish(media, row['titulo'], row['texto'], row['link'])
        pub.setId(int(row['id']))
    
        date_str = row['data_pub']
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        mysql_format = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        
        pub.setData(mysql_format)
        pub.addAvaliacao(int(row['avaliacao']))
        publishs.append(pub)

    return publishs


async def updatePub(publish:Publish):

    req = post('/publicacoes/update', {
        "id":publish.getId(),
        "titulo":publish.getTitulo(),
        "texto":publish.getText(),
        "avaliacao":publish.getAvaliacao(),
        "data_pub":publish.getData()
    })

    return req.code == 200
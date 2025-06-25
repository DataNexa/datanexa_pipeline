from datetime import date

class Publish:

    metadata: dict | None = None

    def __init__(
        self, 
        plataforma:int,
        link:int,
        texto:str,
        temImagem:int | bool,
        temVideo:int | bool,
        dataPublish:date|str|None = None,
        valoracao:int = 0,
        sentimento:int = 0,
        id:int = 0,
        client_id:int = 0,
        metadata:dict = None,
        curtidas:int = 0,
        visualizacoes:int = 0,
        compartilhamento:int = 0,
        monitoramento_id:int = 0,
        comentarios:int = 0
    ):
        
        self.metadata = metadata

        self.data = {
            "client_id": client_id,
            "plataforma": plataforma,
            "link": link,
            "texto": texto,
            "temImagem": temImagem,
            "temVideo": temVideo,
            "dataPublish": dataPublish.isoformat() if isinstance(dataPublish, date) else dataPublish,
            "valoracao": valoracao,
            "sentimento": sentimento,
            "id": id,
            "metadata": metadata if metadata else {},
            "curtidas": curtidas,
            "visualizacoes": visualizacoes,
            "compartilhamento": compartilhamento,
            "monitoramento_id": monitoramento_id,
            "comentarios":comentarios
        }

    def to_dict(self):
        return self.data
    
    def create_by_dict(obj:dict):
        return Publish(
                plataforma=obj.get("plataforma", 0),
                link=obj.get("link", ""),
                texto=obj.get("texto", ""),
                temImagem=int(obj.get("temImagem", False)),
                temVideo=int(obj.get("temVideo", False)),
                dataPublish=obj.get("dataPublish", ""),
                sentimento=obj.get("sentimento", 0),
                id=obj.get("id", 0),
                metadata=obj.get("metadata", {}),
                client_id=obj.get("client_id", 0),
                monitoramento_id=obj.get("monitoramento_id", 0)
            )
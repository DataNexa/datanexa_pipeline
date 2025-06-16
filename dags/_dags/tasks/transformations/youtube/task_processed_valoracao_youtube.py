import math

import logging

from libs.FileManager import FileManager, FileType, LocalFile, read, list_files 
from services.google.youtube.YoutubeService import estatisticas_publicacao

PESOS = {
    "posicao": 1.5,      # Importância da posição no ranking
    "view": 1.0,         # Peso da popularidade
    "like": 2.0,         # Peso dos likes
    "comment": 3.0       # Peso dos comentários
}

def calcular_valoracao(viewCount: int, likeCount: int, commentCount: int, relevancia: int) -> float:


    # Quanto menor a posição (mais acima), maior o score (ex: posição 1 = 100)
    pos_score = relevancia * PESOS["posicao"]

    # Reduzir o impacto de views grandes
    view_score = math.log1p(viewCount) * PESOS["view"]

    like_score = likeCount * PESOS["like"]
    comment_score = commentCount * PESOS["comment"]

    return pos_score + view_score + like_score + comment_score



def task_get_statistics_youtube_publish():


    arquivos = list_files(
        file_type=FileType.processed,
        local=LocalFile.youtube,
    )

    group_clients = {}

    for arquivo in arquivos:

        if not arquivo.endswith("transcrito.json"):
            continue
        
        obj = read(
            file_type=FileType.processed,
            local=LocalFile.youtube,
            filename=arquivo,
        )
        if not obj.get('monitoramento'):
            group_clients[obj['monitoramento']['client_id']] = []
        
        group_clients[obj['monitoramento']['client_id']].append(obj)

    

    for videos in group_clients.values():
        
        videos_ids = []
        youtube_api_key = videos[0].get('monitoramento', {}).get('youtube_api_key', '')
        
        for video in videos:
            video_id = video.get('video_id', '')
            if video_id:
                videos_ids.append(video_id)

        try:
            videos_estatisticas = estatisticas_publicacao(videos_ids, youtube_api_key)
            k = 0
            for video in videos:
                video_id = video.get('video_id', '')
                if video_id and video_id == videos_estatisticas[k]['id']:
                    video['estatisticas'] = videos_estatisticas[k]['statistics']
                    video['valoracao'] = calcular_valoracao(
                        int(video['estatisticas'].get('viewCount', 0)),
                        int(video['estatisticas'].get('likeCount', 0)),
                        int(video['estatisticas'].get('commentCount', 0)),
                        video.get('relevancia', 1)
                    )
                    FileManager(
                        file_type=FileType.processed,
                        local=LocalFile.youtube,
                        content=video,
                        file_ext=f"{video_id}.processed.json"
                    ).save()

        except Exception as e:
            logging.error(f"Erro ao obter estatísticas de publicação: {e}")
            continue

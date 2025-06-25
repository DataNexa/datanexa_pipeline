import math

import logging

from libs.FileManager import FileManager, FileType, LocalFile, read, list_files 
from services.google.youtube.YoutubeService import estatisticas_publicacao
from airflow.operators.python import PythonOperator  # type: ignore


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

    logging.info(f"Arquivos encontrados: {arquivos}")

    group_clients = {}

    for arquivo in arquivos:

        if not arquivo.endswith("transcrito.obj.json"):
            continue
        
        obj = read(
            file_type=FileType.processed,
            local=LocalFile.youtube,
            filename=arquivo,
        )

        logging.info("Processando arquivo: %s", arquivo)

        if not group_clients.get(str(obj['monitoramento']['client_id'])):
            group_clients[str(obj['monitoramento']['client_id'])] = []
        
        
        group_clients[str(obj['monitoramento']['client_id'])].append(obj)

    
    for videos in group_clients.values():
        
        youtube_api_key = ''
        k = 0
        max = len(videos)
        while not youtube_api_key and k < max:
            if videos[k].get('youtube_api_key'):
                youtube_api_key = videos[k].get('youtube_api_key', '')
                break
            k += 1

        if not youtube_api_key:
            logging.error("Nenhuma chave de API do YouTube encontrada nos vídeos.")
            continue
        
        videos_ids = []
        videos_normalizados = {}
        for video in videos:
            video_id = video.get('id', {}).get('videoId', '')
            logging.info(f"Processando vídeo: {video_id}")
            if video_id:
                videos_normalizados[video_id] = video
                videos_ids.append(video_id)

        try:
            logging.info(f"Obtendo estatísticas de publicação para {len(videos_ids)} vídeos.")
            videos_estatisticas = estatisticas_publicacao(videos_ids, youtube_api_key)
            k = 0
            for videoE in videos_estatisticas:
                video = videos_normalizados.get(videoE['id'], "")
                if not video:
                    continue
                video_id = video.get('video_id', '')
                video['estatisticas'] = videoE['statistics']
                video['youtube_api_key'] = ""
                video['valoracao'] = calcular_valoracao(
                    int(videoE['statistics'].get('viewCount', 0)),
                    int(videoE['statistics'].get('likeCount', 0)),
                    int(videoE['statistics'].get('commentCount', 0)),
                    video.get('relevancia', 1)
                )
                logging.info(f"Armazenando video detalhado --- Video ID: {video_id}, Valoracao: {video['valoracao']}")
                FileManager(
                    file_type=FileType.processed,
                    local=LocalFile.youtube,
                    content=video,
                    file_ext=f"{video_id}.processed.json"
                ).save()
                    

        except Exception as e:
            logging.error(f"Erro ao obter estatísticas de publicação: {e}")
            continue


def create_task_processed_valoracao_youtube(dag):
   
    task = PythonOperator(
        task_id="task_processed_valoracao_youtube",
        python_callable=task_get_statistics_youtube_publish,
        dag=dag,
    )

    return task
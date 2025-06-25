from libs.FileManager import FileManager, FileType, LocalFile
from services.google.youtube.YoutubeService import search, YouTubeDork
import logging

def get_data_youtube(monitoramentos):

    for monitoramento in monitoramentos:
        searchObj = monitoramento.get("youtube_search_config", None)
        if not searchObj:
            continue

        dork = YouTubeDork(
            dork=searchObj.get("dork", ""),
            palavrasExatas=searchObj.get("palavrasExatas", []),
            palavrasQuePodeTer=searchObj.get("palavrasQuePodeTer", []),
            videoDuration=searchObj.get("videoDuration", ""),
            videoDefinition=searchObj.get("videoDefinition", ""),
            videoEmbeddable=searchObj.get("videoEmbeddable", ""),
            ytOrder=searchObj.get("order", "relevance"),
            publishedAfter=searchObj.get("publishedAfter", ""),
            lang=searchObj.get("lang", ""),
            youtube_api_key=searchObj.get("youtube_api_key", "")
        )

        results = search(dork)
        
        if results:
            for result in results:
                result['monitoramento'] = {
                    'id': monitoramento['id'],
                    'client_id': monitoramento['client_id']
                }
                results['youtube_api_key'] = searchObj.get("youtube_api_key", "")
                FileManager(
                    file_type=FileType.raw,
                    local=LocalFile.youtube,
                    content=result
                ).save()
        else:
            logging.warning(f"Nenhum resultado encontrado no youtube para o monitoramento {monitoramento['id']}.")
        


def task_get_data_youtube(**kwargs):

    ti = kwargs['ti']
    
    monitoramentos = ti.xcom_pull(task_ids="task_get_monitoramentos_ativos", key='monitoramentos_ativos')
    if not monitoramentos:
        raise ValueError("Nenhum monitoramento ativo encontrado.")
    
    get_data_youtube(monitoramentos) 

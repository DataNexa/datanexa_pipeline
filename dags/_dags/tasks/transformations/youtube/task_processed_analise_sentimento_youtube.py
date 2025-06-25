from libs.FileManager import FileManager, FileType, LocalFile, read, list_files
from services.API.APIGPT import chat
import json
from datetime import date
from time import sleep
from libs.Publish import Publish

from airflow.operators.python import PythonOperator # type: ignore

plataforma = 5  # YouTube

def transform_processed_analise_sentimento_youtube():

    arquivos = list_files(
        file_type=FileType.processed,
        local=LocalFile.youtube,
    )

    publishs = []

    for arquivo in arquivos:

        if not arquivo.endswith("processed.json"):
            continue

        obj = read(
            file_type=FileType.processed,
            local=LocalFile.youtube,
            filename=arquivo
        )

        raw_res = chat(obj)
        publish = json.loads(raw_res)
        dataStr = publish.get("dataPublish", "")
    
        monitoramento = obj.get('monitoramento', {})
        if not monitoramento:
            raise Exception("Monitoramento não foi configurado no arquivo processado para processamento")
        
    
        try:
            partsDate   = dataStr.split("-")
            dataPublish = date(
                year=int(partsDate[0]),
                month=int(partsDate[1]),
                day=int(partsDate[2])
            )
        except Exception:
            dataPublish = None

        publishs.append(
            Publish(
                plataforma=plataforma,
                link=publish.get("link", ""),
                texto=publish.get("texto", ""),
                temImagem=int(publish.get("temImagem", False)),
                temVideo=int(publish.get("temVideo", False)),
                dataPublish=dataPublish,
                sentimento=publish.get("sentimento", 0),
                id=obj.get("id", 0),
                metadata={ },
                valoracao=obj.get("valoracao", 0),
                client_id=monitoramento.get("client_id", 0),
                monitoramento_id=monitoramento.get("id", 0),
                curtidas=obj.get("estatisticas", {}).get("likeCount", 0),
                visualizacoes=obj.get("estatisticas", {}).get("viewCount", 0),
                comentarios=obj.get("estatisticas", {}).get("commentCount", 0),
            ).to_dict()
        )

        sleep(1)

    FileManager(
        file_type=FileType.ready,
        local=LocalFile.youtube,
        content=publishs,
        file_ext="json"
    ).save()


def create_task_transform_processed_youtube(dag):
    return PythonOperator(
        task_id="task_transform_processed_analise_sentimento_youtube",
        python_callable=transform_processed_analise_sentimento_youtube,
        dag=dag,
    )
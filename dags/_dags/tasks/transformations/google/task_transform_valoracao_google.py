from airflow.operators.python import PythonOperator # type: ignore
from libs.FileManager import FileManager, delete, list_files, read, FileType, LocalFile
from libs.Publish import Publish

import logging

plataforma = 1

def transform_valoracao_google():

    arquivos = list_files(
        file_type=FileType.processed,
        local=LocalFile.google
    )

    publishs = []

    for arquivo in arquivos:

        objs:list = read(
            file_type=FileType.processed,
            local=LocalFile.google,
            filename=f"{arquivo}",
        )

        for obj in objs:

            logging.info("Gerando valoração do objeto...")
            logging.info(obj)
           
            metadata = obj.get("metadata", {})
            valoracao = round(100 / int(metadata.get("valorDivisor", 100)), 2)
            
            publishs.append(
                 Publish(
                    plataforma=plataforma,
                    link=obj.get("link", ""),
                    texto=obj.get("texto", ""),
                    temImagem=int(obj.get("temImagem", False)),
                    temVideo=int(obj.get("temVideo", False)),
                    dataPublish=obj.get("dataPublish", ""),
                    sentimento=obj.get("sentimento", 0),
                    id=obj.get("id", 0),
                    metadata=obj.get("metadata", {}),
                    monitoramento_id=obj.get("monitoramento_id", 0),
                    client_id=obj.get("client_id", 0),
                    valoracao=valoracao
                ).to_dict()
            )

    FileManager(
        file_type=FileType.ready,
        local=LocalFile.google,
        content=publishs,
        file_ext="json"
    ).save()

    for arquivo in arquivos:
        delete(
            file_type=FileType.processed,
            local=LocalFile.google,
            filename=f"{arquivo}",
        )

def create_task_transform_valoracao_google(dag):

    task = PythonOperator(
        task_id="task_transform_valoracao_google",
        python_callable=transform_valoracao_google,
        dag=dag,
    )

    return task
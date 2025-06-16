from airflow.operators.python import PythonOperator # type: ignore

from libs.FileManager import list_files, read, delete, FileType, LocalFile
from libs.Publish import Publish
from services.API.APIGPT import chat
from libs.FileManager import FileManager

import logging
from datetime import date
import json 
from time import sleep

import logging

plataforma = 1

def transform_processed_google():

    # carregar os arquivos em data/raw/google

    arquivos = list_files(
        file_type=FileType.raw,
        local=LocalFile.google,
        sufix="/json"
    )

    publishs = []

    for arquivo in arquivos:

        obj = read(
            file_type=FileType.raw,
            local=LocalFile.google,
            filename=f"json/{arquivo}",
        )
        
        req = obj.get('queries', {}).get('request', [])
        if not req or len(req) == 0:
            logging.error(f"Nenhum item encontrado no arquivo {arquivo}. \nNão é possível criar o metadata.")
            continue
        
        monitoramento = obj.get('monitoramento', {})
        if not monitoramento:
            raise Exception("Monitoramento não foi configurado no arquivo bruto para processamento") 

        startIndex = int(req[0].get('startIndex', 1))
        itens = obj.get("items", [])
        i = 0
        
        erro_count = 0
        max_erros = 3
        
        for item in itens:

            if erro_count >= max_erros:
                logging.error(f"Arquivo {arquivo} com muitos erros. Abortando.")
                break
            
            try:
                
                raw_res = chat(item)
                publish = json.loads(raw_res)
                dataStr = publish.get("dataPublish", "")
                
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
                        id=item.get("id", 0),
                        metadata={ "valorDivisor": max(startIndex + i, 1) },
                        client_id=monitoramento.get("client_id", 0),
                        monitoramento_id=monitoramento.get("id", 0)
                    ).to_dict()
                )

                i += 1
                sleep(1)
            
            except Exception as e:  
                erro_count += 1
                logging.error(f"Erro ao processar o item {item.get('id', 'desconhecido')}: {e}")
                continue
        
    # salvar o objeto publish em data/ready/google
    FileManager(
        file_type=FileType.processed,
        local=LocalFile.google,
        content=publishs,
        file_ext="json"
    ).save()

    for arquivo in arquivos:
        delete(
            file_type=FileType.raw,
            local=LocalFile.google,
            filename=f"json/{arquivo}",
        )


def create_task_transform_processed_google(dag):
    
    task = PythonOperator(
        task_id="task_transform_processed_google",
        python_callable=transform_processed_google,
        dag=dag,
        do_xcom_push=False,
    )

    return task

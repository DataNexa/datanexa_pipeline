from libs.FileManager import FileManager, delete, FileType, LocalFile, list_files, read
from services.API.APIDatanexa import APIDatanexa
from libs.Publish import Publish

import logging

from airflow.operators.python import PythonOperator # type: ignore

def create_task_load_ready_data(dag):

    return PythonOperator(
        task_id='task_load_ready_data',
        python_callable=task_load_ready_data,
        dag = dag
    )


def task_load_ready_data():

    arquivos = list_files(
        file_type=FileType.ready
    )

    objErrors = []
    total_arquivos = len(arquivos)
    total_objetos  = 0
    total_registros_success = 0
    total_registros_error   = 0

    for arquivo in arquivos:

        objs:list = read(
            file_type=FileType.ready,
            filename=arquivo
        )

        total_objetos += len(objs)

        for obj in objs:
           
            obj['temImagem'] = obj['temImagem'] == 1
            obj['temVideo'] = obj['temVideo'] == 1
            
            resp = APIDatanexa().post(f"/publicacoes/create?client_id={obj["client_id"]}", obj)

            if resp.code != 200:
                total_registros_error += 1
                objErrors.append(obj)
                logging.warning(f"Erro ao tentar armazenar objeto via API. Codigo: {resp.code()}, mensagem: {resp.message()}")
            
            total_registros_success += 1

        for arquivo in arquivos:
            delete(
                file_type=FileType.ready,
                filename=f"{arquivo}",
            )
        
        logging.info("Armazenamento finalizado:---------------------------")
        logging.info(f"Total de Arquivos: {total_arquivos}")
        logging.info(f"Total de Registros: {total_objetos}")
        logging.info(f"Registros Armazenados: {total_registros_success}")
        logging.info(f"Registros Não Armazenados: {total_registros_error}")

        logging.info(f"Objetos com erros:")
        logging.info(objErrors)
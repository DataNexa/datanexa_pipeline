from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from _dags.tasks.transformations.youtube.task_processed_valoracao_youtube import create_task_processed_valoracao_youtube
import os
from datetime import datetime, timedelta
import logging



def check_and_process(**kwargs):
    path = "/opt/airflow/dags/data/processed/youtube"
    files = os.listdir(path)
    if not files:
        logging.info(f"Nenhum arquivo encontrado em {path}. Task será pulada nesta execução.")
        return
    logging.info(f"{len(files)} arquivo(s) encontrados. Processando...")
    
    # Chama a função que cria e executa a task de valoracao
    task_valoracao_callable = create_task_processed_valoracao_youtube(kwargs['dag'])
    task_valoracao_callable.execute(context=kwargs)


dag = DAG(
    dag_id="dag_processed_valoracao_youtube",
    description="Valoracao de publicações do YouTube",
    schedule=timedelta(minutes=30),  # roda a cada 30 minutos
    catchup=False,
    start_date=datetime(2025, 5, 7),
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["youtube", "valoracao", "processed"],
)

# Task principal: checa arquivos e dispara processamento se houver
sensor_and_process = PythonOperator(
    task_id="task_check_and_process_valoracao",
    python_callable=check_and_process,
    provide_context=True,
    dag=dag,
)
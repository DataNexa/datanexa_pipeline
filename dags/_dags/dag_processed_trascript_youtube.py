from airflow import DAG
from airflow.operators.python import PythonOperator
from _dags.tasks.transformations.youtube.task_transform_transcription_data_youtube import create_task_transform_transcription_data_youtube
from datetime import datetime, timedelta
import os
import logging

def check_and_process_transcription(**kwargs):
    path = "/opt/airflow/dags/data/raw/youtube/json"
    files = os.listdir(path)
    if not files:
        logging.info(f"Nenhum arquivo encontrado em {path}. Task será pulada nesta execução.")
        return
    logging.info(f"{len(files)} arquivo(s) encontrados. Processando transcrição...")
    
    # Cria e executa a task de transcrição
    task_transcription_callable = create_task_transform_transcription_data_youtube(kwargs['dag'])
    task_transcription_callable.execute(context=kwargs)


dag = DAG(
    dag_id="dag_processed_transcript_youtube",
    description="Transcrição de vídeos do YouTube",
    schedule=timedelta(minutes=30),  # roda a cada 30 minutos
    catchup=False,
    start_date=datetime(2025, 5, 7),
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["youtube", "transcript", "processed"],
)


task_sensor_and_process = PythonOperator(
    task_id="task_check_and_process_transcription",
    python_callable=check_and_process_transcription,
    provide_context=True,
    dag=dag,
)
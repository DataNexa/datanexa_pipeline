
from airflow import DAG # type: ignore
from airflow.sensors.filesystem import FileSensor # type: ignore
from airflow.operators.python import PythonOperator # type: ignore

from datetime import datetime, timedelta
import os

from _dags.tasks.transformations.google.task_transform_processed_google import create_task_transform_processed_google
from _dags.tasks.transformations.google.task_transform_valoracao_google import create_task_transform_valoracao_google

default_args = {
    "start_date": datetime(2025, 5, 7),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="dag_processed_google",
    description="Criação de publicações processadas do Google Search",
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["google", "transformation", "processed"],
)

sensor_processed_google = FileSensor(
    task_id="task_sensor_processed_google",
    fs_conn_id="filesystem_default",
    filepath="/opt/airflow/dags/data/raw/google/json/*",
    poke_interval=60,  # Intervalo de verificação em segundos
    timeout=600,  # Tempo máximo de espera em segundos
    mode="poke",  # Modo de operação do sensor
    dag=dag,
)


task_transform_processed_google = create_task_transform_processed_google(dag)
task_transfrom_valoracao_google = create_task_transform_valoracao_google(dag)
sensor_processed_google >> task_transform_processed_google >> task_transfrom_valoracao_google
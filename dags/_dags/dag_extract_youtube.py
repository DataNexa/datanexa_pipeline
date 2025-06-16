from airflow import DAG  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from tasks.task_get_data_youtube import task_get_data_youtube  # type: ignore

import logging 

from datetime import datetime, timedelta
from _dags.tasks.task_get_monitoramentos_ativos import create_task_get_monitoramentos
from services.google.youtube.YoutubeService import YoutubeService

default_args = {
        "start_date": datetime(2025, 5, 7),
        "retries": 2,
        "retry_delay": timedelta(minutes=1)
    }


dag = DAG(
    dag_id="dag_extract_youtube",
    description="Extração de dados do YouTube",
    schedule='180 * * * *', 
    catchup=False,
    default_args=default_args,
    tags=["extração", "datanexa", "youtube"]
)

task1 = create_task_get_monitoramentos(dag)

task2 = PythonOperator(
    task_id="task_get_data_youtube",
    python_callable=task_get_data_youtube,
    provide_context=True,
    dag=dag,
    do_xcom_push=False
)

task1 >> task2
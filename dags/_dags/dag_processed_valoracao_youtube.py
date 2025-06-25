from airflow import DAG # type: ignore
from airflow.sensors.filesystem import FileSensor # type: ignore
from _dags.tasks.transformations.youtube.task_processed_valoracao_youtube import create_task_processed_valoracao_youtube

from datetime import datetime, timedelta

dag = DAG(
    dag_id="dag_processed_valoracao_youtube",
    description="Valoracao de publicações do YouTube",
    schedule=None,
    catchup=False,
    default_args={
        "start_date": datetime(2025, 5, 7),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["youtube", "valoracao", "processed"],
)

sensor_processed_valoracao_youtube = FileSensor(
    task_id="task_sensor_processed_valoracao_youtube",
    fs_conn_id="filesystem_default",
    filepath="/opt/airflow/dags/data/processed/youtube/*",
    poke_interval=60,
    timeout=10,
    mode="reschedule",
    dag=dag,
)

task_valoracao = create_task_processed_valoracao_youtube(dag)

sensor_processed_valoracao_youtube >> task_valoracao
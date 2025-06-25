from datetime import datetime, timedelta
from airflow import DAG  # type: ignore
from airflow.sensors.filesystem import FileSensor  # type: ignore
from _dags.tasks.transformations.youtube.task_processed_analise_sentimento_youtube import create_task_transform_processed_youtube

dag = DAG(
    dag_id="dag_processed_youtube",
    description="Criação de publicações processadas com analise de sentimento do YouTube",
    schedule=None,
    catchup=False,
    default_args={
        "start_date": datetime(2025, 5, 7),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["youtube", "transformation", "processed", "analise", "sentimento"],
)

sensor_processed_youtube = FileSensor(
    task_id="task_sensor_processed_youtube",
    fs_conn_id="filesystem_default",
    filepath="/opt/airflow/dags/data/processed/youtube/*",
    poke_interval=60,
    timeout=10,
    mode="reschedule",
    dag=dag,
)

task_transform_processed_youtube = create_task_transform_processed_youtube(dag)

sensor_processed_youtube >> task_transform_processed_youtube
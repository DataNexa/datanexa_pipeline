
from airflow import DAG # type: ignore
from airflow.sensors.filesystem import FileSensor # type: ignore

from _dags.tasks.transformations.youtube.task_transform_transcription_data_youtube import create_task_transform_transcription_data_youtube

from datetime import datetime, timedelta


dag = DAG(
    dag_id="dag_processed_transcript_youtube",
    description="Transcrição de vídeos do YouTube",
    schedule=None,
    catchup=False,
    default_args={
        "start_date": datetime(2025, 5, 7),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["youtube", "transcript", "processed"],
)


sensor_processed_transcript_youtube = FileSensor(
    task_id="task_sensor_processed_transcript_youtube",
    fs_conn_id="filesystem_default",
    filepath="/opt/airflow/dags/data/raw/youtube/json/*",
    poke_interval=60,
    timeout=10,
    mode="reschedule",
    dag=dag,
)

task_transcription = create_task_transform_transcription_data_youtube(dag)

sensor_processed_transcript_youtube >> task_transcription
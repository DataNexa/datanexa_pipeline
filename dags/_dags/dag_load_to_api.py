from airflow import DAG #type: ignore
from airflow.sensors.filesystem import FileSensor #type: ignore

from _dags.tasks.task_load_ready_data import create_task_load_ready_data 

from datetime import datetime, timedelta

default_args = {
    "start_date":datetime(2025, 5, 7)
}

dag = DAG(
    dag_id="dag_load_to_api",
    description="Armazenamento de dados na API",
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["armazenar", "datanexa", "api"]
)


sensor_ready_files = FileSensor(
    task_id="task_sensor_ready_file",
    fs_conn_id="filesystem_default",
    filepath="/opt/airflow/dags/data/ready/*",
    poke_interval=60,
    timeout=10,
    mode="reschedule",
    dag=dag
)

task_load_ready_data = create_task_load_ready_data(dag)

sensor_ready_files >> task_load_ready_data



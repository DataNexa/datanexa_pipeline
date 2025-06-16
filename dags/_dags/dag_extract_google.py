from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore

from datetime import datetime, timedelta

from _dags.tasks.task_get_monitoramentos_ativos import create_task_get_monitoramentos
from tasks.task_get_data_google import task_google_extract_and_save_raw

default_args = {
    "start_date": datetime(2025, 5, 7),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="dag_extract_google",
    description="Extração de dados do Google Search",
    schedule="0 9,14 * * *",
    catchup=False,
    default_args=default_args,
    tags=["google", "extract"],
)

t1 = create_task_get_monitoramentos(dag)

t2 = PythonOperator(
    task_id="task_salvar_raw_data_google",
    python_callable=task_google_extract_and_save_raw,
    dag=dag
)

t1 >> t2

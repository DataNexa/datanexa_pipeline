from airflow.operators.python import PythonOperator # type: ignore
import logging
from services.API.APIDatanexa import APIDatanexa

def task_get_monitoramentos(**kwargs):
    
    response = APIDatanexa().get("monitoramentos/readAll")
    
    if response.status_code != 200:
        logging.error(f"Erro ao obter monitoramentos ativos: {response.message}")
        raise ValueError(f"Erro ao obter monitoramentos ativos: {response.message}")

    logging.info(f"Monitoramentos ativos:\n {response.body}")

    ti = kwargs['ti']
    ti.xcom_push(key='monitoramentos_ativos', value=response.body)


def create_task_get_monitoramentos(dag):

    return PythonOperator(
        task_id='task_get_monitoramentos_ativos',
        python_callable=task_get_monitoramentos,
        dag=dag
    )
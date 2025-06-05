from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore

from datetime import datetime, timedelta

from _dags.tasks.task_get_monitoramentos_ativos import create_task_get_monitoramentos
from libs.FileManager import FileManager, FileType, LocalFile
from services.google.search.GoogleService import Dork, search

defaultNotInSites = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "linkedin.com",
    "wikipedia.org",
    "amazon.com",
    "ebay.com",
    "yahoo.com",
    "bing.com"
]

def salvar_raw_data_google(**kwargs):

    ti = kwargs['ti']
    
    monitoramentos = ti.xcom_pull(task_ids="task_get_monitoramentos_ativos", key='monitoramentos_ativos')
    if not monitoramentos:
        raise ValueError("Nenhum monitoramento ativo encontrado.")

    maxPages = 10
    for monitoramento in monitoramentos:

        searchObj = monitoramento.get("google_search_config", None)
        if not searchObj:
            continue

        notInSites = searchObj.get("notInSites", [])
        notInSites.extend(defaultNotInSites)

        dork = Dork(
            sites=searchObj.get("sites", []),
            notSites=notInSites,
            inurl=searchObj.get("inUrl", ""),
            intitle=searchObj.get("inTitle", ""),
            intext=searchObj.get("inText", ""),
            exatamente=searchObj.get("palavrasExatas", ""),
            podeter=searchObj.get("palavrasQuePodeTer", ""),
            naoConter=searchObj.get("excluirPalavras", ""),
            dork=searchObj.get("dork", "")
        )

        pg = 1
        while pg < maxPages:
            results = search(dork, page=pg)
            if results['searchInformation']['totalResults'] == '0':
                break
            pg += 1
            FileManager(
                file_type=FileType.raw,
                local=LocalFile.google,
                content=str(results),
                file_ext="json"
            ).save()


default_args = {
    "start_date": datetime(2025, 5, 7),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="dag_extract_google",
    description="Extração de dados do Google Search",
    schedule="* 9,14 * * *",
    catchup=False,
    default_args=default_args,
    tags=["google", "extract"],
)

t1 = create_task_get_monitoramentos(dag)

t2 = PythonOperator(
    task_id="task_salvar_raw_data_google",
    python_callable=salvar_raw_data_google,
    dag=dag
)

t1 >> t2

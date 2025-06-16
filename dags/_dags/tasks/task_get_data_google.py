
from libs.FileManager import FileManager, FileType, LocalFile
from services.google.search.GoogleService import Dork, search
from libs.Metadata import add_metadata

import logging

defaultNotInSites = [
    "threads.net",
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
    "bing.com",
    "desciclopedia.org",
    "x.com",
    "tiktok.com"
]

def google_extract_and_save_raw(monitoramentos):

    #maxPages = 10
    maxPages = 1
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
        while pg <= maxPages:
            
            results = search(dork, page=pg)
            logging.info(f"Página {pg} - Resultados: {results['searchInformation']['totalResults']}")

            if results['searchInformation']['totalResults'] == '0' or 'nextPage' not in results['queries']:
                break
            
            result_with_meta = add_metadata(monitoramento, results)
            if not result_with_meta:
                raise ValueError("Erro ao adicionar metadata ao resultado da pesquisa.")
                
            pg += 1
            FileManager(
                file_type=FileType.raw,
                local=LocalFile.google,
                content=result_with_meta,
                file_ext="json"
            ).save()

def task_google_extract_and_save_raw(**kwargs):

    ti = kwargs['ti']
    
    monitoramentos = ti.xcom_pull(task_ids="task_get_monitoramentos_ativos", key='monitoramentos_ativos')
    if not monitoramentos:
        raise ValueError("Nenhum monitoramento ativo encontrado.")
    
    google_extract_and_save_raw(monitoramentos)

    
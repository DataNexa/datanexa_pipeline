from libs.Config import Config
from time import sleep
from services.API.APIDatanexa import APIDatanexa
from services.google.search.GoogleService import Dork, search

config = Config()

response = APIDatanexa().get("monitoramentos/readAll")

body = response.body()

for monitoramento in body:

    searchObj = monitoramento.get("google_search_config", None)
    
    if not searchObj:
        continue
    
    dork = Dork(
        sites=searchObj.get("sites", []),
        notSites=searchObj.get("notInSites", []),
        inurl=searchObj.get("inUrl", ""),
        intitle=searchObj.get("inTitle", ""),
        intext=searchObj.get("inText", ""),
        exatamente=searchObj.get("palavrasExatas", ""),
        podeter=searchObj.get("palavrasQuePodeTer", ""),
        naoConter=searchObj.get("excluirPalavras", ""),
        dork=searchObj.get("dork", "")
    )

    pg = 1
    while pg < 6:
        results = search(dork, page=pg)
        # ['kind', 'url', 'queries', 'context', 'searchInformation', 'items']
        if results['searchInformation']['totalResults'] == '0':
            break
        pg += 1
        print(results['items'][0])
        sleep(2)  # Pausa de 2 segundos entre as páginas
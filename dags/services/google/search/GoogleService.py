# https://www.googleapis.com/customsearch/v1?key={k}&cx={cx}&q={q}&sort=date
from typing import TypedDict
from services.google.search.GoogleClient import GoogleClient
import requests
import logging


class Dork(TypedDict):
    sites:list
    notSites:list
    inurl:str
    intitle:str
    intext:str
    exatamente:str
    podeter:str 
    naoConter:str 
    dork:str


def tranform_to_dork_string(obj: Dork) -> str:

    if obj.get("dork"):
        return obj["dork"].strip()

    parts = []

    if obj.get("sites"):
        sites = [s.strip() for s in obj["sites"] if s.strip()]
        if sites:
            parts.append("(" + " OR ".join(f"site:{site}" for site in sites) + ")")

    if obj.get("notSites"):
        not_sites = [s.strip() for s in obj["notSites"] if s.strip()]
        if not_sites:
            parts.append(" ".join(f"-site:{site}" for site in not_sites))

    if obj.get("inurl"):
        parts.append(f"inurl:{obj['inurl'].strip()}")

    if obj.get("intitle"):
        parts.append(f"intitle:{obj['intitle'].strip()}")

    if obj.get("intext"):
        parts.append(f"intext:{obj['intext'].strip()}")

    if obj.get("exatamente"):
        ex = obj["exatamente"].strip()
        # Mantém aspas se já houver
        if not (ex.startswith('"') and ex.endswith('"')):
            ex = f'"{ex}"'
        parts.append(ex)

    if obj.get("podeter"):
        podeter_words = obj["podeter"].strip().split()
        parts.extend(podeter_words)

    if obj.get("naoConter"):
        nao_conter_words = obj["naoConter"].strip().split()
        parts.extend(f"-{word}" for word in nao_conter_words)

    return " ".join(parts).strip()


def search(dorkObj:Dork, sort:str="date", page:int = 1):

    try:
        q = tranform_to_dork_string(dorkObj)
        client = GoogleClient()
        url = client.getUrlSearch(q, sort, page)
        response = requests.get(url, timeout=10)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        logging.error(f"[ERRO HTTP] {e.response.status_code} - {e.response.text}")
        raise

    except requests.exceptions.RequestException as e:
        logging.error(f"[ERRO DE REDE] {str(e)}")
        raise

    except Exception as e:
        logging.error(f"[ERRO GERAL] {str(e)}")
        raise
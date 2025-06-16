
from typing import TypedDict, Optional, List
from datetime import time
import requests
import logging

API_URL = "https://www.googleapis.com/youtube/v3/search"

class YouTubeDork(TypedDict):
    dork: str
    palavrasExatas: List[str]
    palavrasQuePodeTer: List[str]
    videoDuration: Optional[str]  # 'any' | 'short' | 'medium' | 'long'
    videoDefinition: Optional[str]  # 'any' | 'high' | 'standard'
    videoEmbeddable: Optional[bool]
    ytOrder: Optional[str]  # 'date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'
    publishAfter: Optional[str]  # ISO 8601: "2025-01-01T00:00:00Z"
    lang: Optional[str]  # ISO 639-1 'en', 'pt', 'es'
    youtube_api_key: str


def build_youtube_dork_query(dork: YouTubeDork) -> str:

    partes = []

    if dork.get("dork"):
        return dork["dork"].strip()

    if dork.get("palavrasExatas"):
        for frase in dork["palavrasExatas"]:
            clean = frase.strip()
            if clean:
                if not (clean.startswith('"') and clean.endswith('"')):
                    clean = f'"{clean}"'
                partes.append(clean)

    if dork.get("palavrasQuePodeTer"):
        for word in dork["palavrasQuePodeTer"]:
            clean = word.strip()
            if clean:
                partes.append(clean)

    return " ".join(partes).strip()
    

def youtube_search_with_pagination(params, max_pages=3) -> list:
    
    next_page_token = None
    page = 1
    multiplicador_de_relevancia_da_pagina = max_pages

    datas = []

    while page <= max_pages:

        relevancia = 100 * multiplicador_de_relevancia_da_pagina

        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(API_URL, params=params)
        data = response.json()
        data['metadata'] = {
            "relevancia": relevancia,
        }
        datas.append(data)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            print("Não há mais páginas.")
            break

        page += 1
        multiplicador_de_relevancia -= 1
        time.sleep(1)

    return datas

def estatisticas_publicacao(videos_ids:list, youtube_api_key:str) -> list:
    """
        {
            "items": [
                {
                    "id": "abc123DEF456",
                    "statistics": {
                        "viewCount": "15234",
                        "likeCount": "532",
                        "commentCount": "89"
                    }
                },
                {
                    "id": "ghi789JKL012",
                    "statistics": {
                        "viewCount": "4837",
                        "likeCount": "198",
                        "commentCount": "32"
                    }
                }
            ]
        }
    """
    ids = ",".join(videos_ids)
    params = {
        "part": "statistics",
        "id": ids,
        "key": youtube_api_key
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    resp = response.json()
    return resp.get("items", [])
        


def build_youtube_search_params(dork: YouTubeDork, max_results: int = 50) -> dict:
    query_string = build_youtube_dork_query(dork)
    params = {
        "part": "snippet",
        "q": query_string,
        "type": "video",
        "maxResults": max_results,
        "key": dork["youtube_api_key"],
    }

    if dork.get("videoDuration"):
        params["videoDuration"] = dork["videoDuration"]

    if dork.get("videoDefinition"):
        params["videoDefinition"] = dork["videoDefinition"]

    if dork.get("videoEmbeddable") is not None:
        params["videoEmbeddable"] = "true" if dork["videoEmbeddable"] else "false"

    if dork.get("ytOrder"):
        params["order"] = dork["ytOrder"]

    if dork.get("publishAfter"):
        params["publishedAfter"] = dork["publishAfter"]

    if dork.get("lang"):
        params["relevanceLanguage"] = dork["lang"]

    return params


def search(dork: YouTubeDork) -> list:

    params = build_youtube_search_params(dork)
    logging.info(f"Query enviada para API:\n{params}\n")

    return youtube_search_with_pagination(params)




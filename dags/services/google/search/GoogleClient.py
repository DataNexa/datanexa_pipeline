import os
from dotenv import load_dotenv
import urllib.parse

def transform_dork_to_url_query(dork: str) -> str:

    parts = []
    tokens = dork.split()

    temp_phrase = []
    in_quotes = False

    for token in tokens:
        if token.startswith('"') and not in_quotes:
            in_quotes = True
            temp_phrase = [token.strip('"')]
        elif token.endswith('"') and in_quotes:
            temp_phrase.append(token.strip('"'))
            phrase = " ".join(temp_phrase)
            parts.append(f'"{phrase}"')
            in_quotes = False
        elif in_quotes:
            temp_phrase.append(token)
        else:
            parts.append(token)

    if in_quotes and temp_phrase:
        phrase = " ".join(temp_phrase)
        parts.append(f'"{phrase}"')

    encoded = [urllib.parse.quote_plus(part) for part in parts]
    return "+".join(encoded)


class GoogleClient:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return

        load_dotenv()

        ctx_env = 'GOOGLE_SEARCH_API_CX'
        key_env = 'GOOGLE_SEARCH_API_KEY'

        self.ctx_google = os.getenv(ctx_env)
        self.key_google = os.getenv(key_env)

        if not self.ctx_google or not self.key_google:
            raise ValueError("Variáveis de ambiente não definidas corretamente.")

        self.initialized = True

    def getUrlSearch(self, q: str, sort: str, page: int = 1) -> str:

        query = transform_dork_to_url_query(q)
        start_index = (page - 1) * 10 + 1  

        return (
            f'https://www.googleapis.com/customsearch/v1'
            f'?key={self.key_google}&cx={self.ctx_google}&q={query}&sort={sort}&start={start_index}'
        )
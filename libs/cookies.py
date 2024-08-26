import asyncio
from typing import List, Optional

class Cookie:
    def __init__(self, email: str, senha:str, site: str):
        self.senha = senha
        self.email = email
        self.arquivo = email+"."+site+".json"
        self.site = site

class CookieManager:

    _instance: Optional['CookieManager'] = None

    cookies:list[Cookie] = []

    def __new__(cls, cookies: List[Cookie]):
        if cls._instance is None:
            cls._instance = super(CookieManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, cookies: List[Cookie]):
        if not self._initialized:
            self.cookies = cookies
            self.uso = [False] * len(cookies)
            self.lock = asyncio.Lock()
            self._initialized = True

    async def pegarCookieLivre(self, site:str):
        async with self.lock:
            for i, em_uso in enumerate(self.uso):
                if not em_uso and self.cookies[i].site == site:
                    self.uso[i] = True
                    return self.cookies[i]
            raise Exception("Nenhum cookie disponível")

    async def liberarCookie(self, cookie:Cookie):
        async with self.lock:
            index = self.cookies.index(cookie)
            if index >= 0:
                self.uso[index] = False
            else:
                raise Exception("Cookie não encontrado")
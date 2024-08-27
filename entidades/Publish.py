import re

def extrair_numero(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

class Publish:

    _midiaSlug:str
    _monitoramento_id:int
    _avaliacao:int = 0 # 0 - negativo | 1 - neutro | 2 - positivo
    _text:str = ""
    _data:str = ""
    _titulo:str = ""
    link:str = ""

    def __init__(self, midiaSlug:str, titulo:str, text:str, link:str) -> None:
        self._titulo = titulo
        self._midiaSlug = midiaSlug
        self._text = text
        self.link = link

    def getMidiaSlug(self):
        return self._midiaSlug
    
    def getData(self):
        return self._data

    def getTitulo(self):
        return self._titulo

    def getAvaliacao(self) -> int:
        return self._avaliacao
    
    def setAvaliacao(self, avaliacao:str) -> None:
        num = extrair_numero(avaliacao)
        if num is None or num > 2 or num < 0:
            self._avaliacao = 1
        self._avaliacao = num

    def setData(self, data:str) -> None:
        self._data = data

    def setTexto(self, texto:str) -> None:
        self._text = texto

    def __eq__(self, other):
        if isinstance(other, Publish):
            return self.link == other.link
        return False

    def __hash__(self):
        return hash(self.link)
    
    def getLink(self):
        return self.link
    
    def getText(self):
        return self._text

    def toString(self) -> str:
        return f"""
        =======================================================
            midia:{self._midiaSlug}
            avaliacao:{self._avaliacao}
            link:{self.link}
            data:{self._data}
        """
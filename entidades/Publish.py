class Publish:

    _midiaSlug:str
    _monitoramento_id:int
    _avaliacao:int = 0 # 0 - neutro ou não identificado | 1 - positivo | 2 - negativo
    _text:str = ""
    _data:str = ""
    _link:str = ""

    def __init__(self, midiaSlug:str, text:str, link:str) -> None:
        self._midiaSlug = midiaSlug
        self._text = text
        self._link = link

    def getMidiaSlug(self):
        return self._midiaSlug
    
    def setAvaliacao(self, avaliacao:int) -> None:
        self._avaliacao = avaliacao

    def setData(self, data:str) -> None:
        self._data = data

    def toString(self) -> str:
        return f"""
        =======================================================
            midia:{self._midiaSlug}
            avaliacao:{self._avaliacao}
            link:{self._link}
            data:{self._data}
        -------------------------------------------------------
        texto:
        -------------------------------------------------------
        {self._text}
        =======================================================
        """
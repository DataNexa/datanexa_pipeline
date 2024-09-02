from libs.navigator import Navigator
from entidades.Publish import Publish
from datetime import datetime, timedelta
import re


def transformar_data(data):

    meses = {
        'jan.': 1, 'fev.': 2, 'mar.': 3, 'abr.': 4, 'mai.': 5,
        'jun.': 6, 'jul.': 7, 'ago.': 8, 'set.': 9, 'out.': 10,
        'nov.': 11, 'dez.': 12
    }

    def tratar_data_extensa(data_extensa):
        partes = data_extensa.split()
        if len(partes) == 5 and partes[1] == 'de' and partes[3] == 'de':
            dia = int(partes[0])
            mes = meses.get(partes[2], None)
            ano = int(partes[4])
            if mes:
                return datetime(ano, mes, dia).strftime('%Y-%m-%d %H:%M:%S')
        return None

    def tratar_data_relativa(data_relativa):
        data_referencia = datetime.now()
        match = re.match(r'(\d+)\s*(dia|dias|mês|meses|ano|anos)', data_relativa, re.IGNORECASE)
        if match:
            quantidade = int(match.group(1))
            unidade = match.group(2).lower()
            
            if unidade in ['dia', 'dias']:
                data_resultado = data_referencia + timedelta(days=quantidade)
            elif unidade in ['semana', 'semanas']:
                data_resultado = data_referencia + timedelta(weeks=quantidade)
            elif unidade in ['mês', 'meses']:
                data_resultado = data_referencia + timedelta(weeks=4 * quantidade)  
            elif unidade in ['ano', 'anos']:
                data_resultado = data_referencia + timedelta(weeks=52 * quantidade) 
            return data_resultado.strftime('%Y-%m-%d %H:%M:%S')
        return None

    resultado = tratar_data_extensa(data)
    if resultado:
        return resultado

    resultado = tratar_data_relativa(data)
    if resultado:
        return resultado

    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def search(navigator:Navigator):
    linksa = navigator.findElements('xpath', "//div[@role='listitem']", 3)
    if linksa == False:
        return
    for link in linksa:
        if link.getText() == 'Notícias':
            link.click()

    navigator.sleep(4)


def get_all_publish(navigator:Navigator, page:int, base:str):

    
    startnum = 10 * page
    startstr = "&start="

    navigator.goto(base+startstr+str(startnum), True)
    
    pubs:list[Publish] = []

    elementsLinks = navigator.findElements('xpath', "//*[@id='search']//a", 3)
    if elementsLinks == False:
        return pubs
    
    temppubs:list[Publish] = []

    for el in elementsLinks:

        tituloAll  = el.getText()
        tituloAll  = tituloAll.replace("\n", " - ")
        tituloPart = tituloAll.split("...")
        titulo     = tituloPart[0]

        datael     = navigator.findElements('tag', "span", 3, el)
        if datael == False or len(datael) < 3:
            continue

        datast     = datael[2].getText()
        data       = transformar_data(datast)

        link       = el.getValueOf('href')
        pub        = Publish("web", titulo, '', link)
        pub.setData(data)
        temppubs.append(pub)

    for p in temppubs:

        navigator.goto(p.getLink(), True)
        navigator.sleep(3)
        textoe = navigator.findElement("tag", "article",5)
        if textoe == False:
            continue

        texto  = textoe.getText()
        p.setTexto(texto)
        pubs.append(p)

    navigator.goto(base, True)
    navigator.sleep(3)
    return pubs
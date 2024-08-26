
from entidades.Publish import Publish
from datetime import datetime, timedelta

from libs.navigator import Navigator, Element
from youtube_transcript_api import YouTubeTranscriptApi
import re


# ytd-item-section-renderer
#    div#contents | div[2]
#       ytd-video-renderer

# data e visualização: 
# ytd-video-meta-block

HOJE_FILTRO = "&sp=EgQIAhAB"
POR_VISUALIZACOES = "&sp=CAMSAhAB"

UNIQUE_LINKS = []

def get_video_id(link:str):

    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|.+\?v=)?([\w-]{11})'
    match = re.search(pattern, link)
    
    if match:
        try:
            return match.group(1)
        except:
            return False
    return False


def get_text_video(video_id:str) :
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    full_text = "\n".join([entry['text'] for entry in transcript])
    return full_text


def add_data_publish(navigator:Navigator, el:Element, publish:Publish) -> None:

    datael = navigator.findElements("xpath", "//*[@id='metadata-line']//span", 3, el)
    now = datetime.now()

    if datael == False or len(datael) < 2:
        publish.setData(now.strftime('%Y-%m-%d 00:00:00'))
        return
    
    strdata = datael[1].getText()
    match = re.match(r'(\d+)\s*(dias?|semanas?|meses?|anos?)', strdata)
    
    if not match:
        publish.setData(now.strftime('%Y-%m-%d 00:00:00'))
        return
    
    quantidade = int(match.group(1))
    periodo = match.group(2).lower()
    
    if 'dia' in periodo:
        delta = timedelta(days=quantidade)
    elif 'semana' in periodo:
        delta = timedelta(weeks=quantidade)
    elif 'mes' in periodo:
        delta = timedelta(days=30 * quantidade)
    elif 'ano' in periodo:
        delta = timedelta(days=365 * quantidade)
    else:
        publish.setData(now.strftime('%Y-%m-%d 00:00:00'))
        return
    
    result_date = now - delta
    publish.setData(result_date.strftime('%Y-%m-%d 00:00:00'))



def get_list_publish(navigator:Navigator) -> list[Publish]:

    navigator.sleep(4)

    elementsVideo = navigator.findElements("tag", "ytd-video-renderer")
    lista:list[Publish] = []

    for el in elementsVideo:
        
        tagsa = navigator.findElements("tag", "a", 2, el)
        if len(tagsa) < 5: continue 
        
        taga  = tagsa[1]
        linka = taga.getValueOf("href")
        v_id  = get_video_id(linka)
        link  = f"https://www.youtube.com/watch?v={v_id}"
        
        if link in UNIQUE_LINKS: continue
        UNIQUE_LINKS.append(link)

        title = taga.getValueOf("title")
        text  = get_text_video(v_id)
        pub   = Publish("youtube", title, text, link)
        add_data_publish(navigator, el, pub)
        print(pub.getData())
        lista.append(pub)

    return lista 


def search(navigator:Navigator, expressao:str, hoje=False):
    expressao = expressao.replace(" ", "+")
    navigator.goto(f"results?search_query={expressao}{HOJE_FILTRO if hoje else POR_VISUALIZACOES}")


def continuar(navigator:Navigator) -> bool:
    return navigator.findElement('id', 'message', 3) == False
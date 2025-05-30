from dags.services.API.APIDatanexa import APIDatanexa
from dags.services.google.search.GoogleService import Dork, search
from time import sleep


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

"""
{   
    'kind': 'customsearch#result', 
    'title': 'Serpro é um dos destaques da Campus Party Brasília 2024', 
    'htmlTitle': 'Serpro é um dos destaques da Campus Party Brasília 2024', 
    'link': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party', 
    'displayLink': 'www.serpro.gov.br', 
    'snippet': 'Mar 26, 2024 ... Festa da tecnologia. O Serpro é um parceiro tradicional nos eventos nacionais e regionais da Campus Party, que ocorrem no país desde 2008. “É\xa0...', 
    'htmlSnippet': 'Mar 26, 2024 <b>...</b> <b>Festa</b> da tecnologia. O Serpro é um parceiro tradicional nos eventos nacionais e regionais da Campus Party, que ocorrem no país desde 2008. “É&nbsp;...', 
    'formattedUrl': 'https://www.serpro.gov.br/menu/noticias/noticias.../serpro-campus-party', 
    'htmlFormattedUrl': 'https://www.serpro.gov.br/menu/noticias/noticias.../serpro-campus-party', 
    'pagemap': {
        'cse_thumbnail': [
            {
                'src': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5LXLC28d814qG3bP1xfyqHjSoqZ5tMnSbSiktowpyVGpbeqdWNuTn2zY&s', 
                'width': '310', 'height': '162'
            }
        ], 
        'Article': [
            {
                'alternativeHeadline': 'Tecnologia', 
                'articleBody': 'A 6ª edição da Campus Party acontece em Brasília, de 27 a 31 de março, e, em homenagem aos 50 anos do planetário da capital federal, vai trazer convidados para falar sobre astronomia,...', 
                'description': 'Maior empresa pública de TI do país será responsável por palestras sobre programação no jogo Fortnite, empreendedorismo e inteligência artificial generativa', 
                'dateModified': '27 de março de 2024', 
                'articleSection': 'Notícia', 
                'headline': 'Serpro é um dos destaques da Campus Party Brasília 2024'
            }
        ], 
        'metatags': [
            {
                'og:image': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party/@@images/image/large', 
                'twitter:card': 'summary_large_image', 
                'twitter:title': 'Serpro é um dos destaques da Campus Party Brasília 2024', 
                'og:image:width': '768', 
                'og:type': 'article', 
                'twitter:url': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party', 
                'og:title': 'Serpro é um dos destaques da Campus Party Brasília 2024', 
                'og:image:height': '511', 
                'og:description': 'Maior empresa pública de TI do país será responsável por palestras sobre programação no jogo Fortnite, empreendedorismo e inteligência artificial generativa', 
                'twitter:image': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party/@@images/image/preview', 
                'twitter:site': '@SERPRO', 
                'viewport': 'width=device-width, initial-scale=1.0', 
                'twitter:description': 'Maior empresa pública de TI do país será responsável por palestras sobre programação no jogo Fortnite, empreendedorismo e inteligência artificial generativa', 
                'og:locale': 'pt_BR', 
                'og:url': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party'
            }
        ], 
        'cse_image': [
            {
                'src': 'https://www.serpro.gov.br/menu/noticias/noticias-2024/serpro-campus-party/@@images/image/large'
            }
        ]
    }
}
"""
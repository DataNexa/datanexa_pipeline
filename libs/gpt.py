
from entidades.Publish import Publish
import openai
import time
from openai.error import RateLimitError
from libs.config import Config
from libs.request import post

def count_tokens(texto:str) -> int:
    return int(len(texto.split()) * 1.33)

def filtrar_publicacoes(publish_list:list[Publish], links_nao_usados:list[str]):

    publicacoes_filtradas:list[Publish] = []

    for pub in publish_list:
        if pub is not None and pub.getLink() in links_nao_usados:
            publicacoes_filtradas.append(pub)

    return publicacoes_filtradas


def analise(monitoramento_id:int, publicacoes: list[Publish], alvo: str) -> list[Publish]:

    links_pubs = []
    for pub in publicacoes: 
        if pub is not None:
            links_pubs.append(pub.getLink())

    req = post('/publicacoes/filter', {
        "monitoramento_id":monitoramento_id,
        "links": links_pubs
    })

    filtrados = []

    if req.code == 200:
        lista = list(req.body)
        filtrados = filtrar_publicacoes(publicacoes,lista)

    openai.api_key = Config().getAccount('keygpt')
    
    max_tokens = 7000 
    
    for pub in filtrados:
        
        if pub is None:
            continue

        texto = pub.getText()
        
        if count_tokens(texto) > max_tokens:
            # Dividir o texto em partes menores se necessário
            partes_texto = [texto[i:i+max_tokens] for i in range(0, len(texto), max_tokens)]
        else:
            partes_texto = [texto]
        
        avaliacao = ''
        
        parte = partes_texto[0]
        limite_tentativas = 2
        tentativas = 0
        
        while True:
            
            if tentativas > limite_tentativas:
                print("A quantidade de tentativas para análise foi expirada.")
                break 

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": f" Em relação a {alvo}, analise o texto com uma resposta curta classificando como '0' para negativo, '2' para positivo e '1' para neutro ou indeterminado \n texto: {parte}"
                        }
                    ]
                )
                avaliacao = response.choices[0].message.content
                break 

            except RateLimitError:
                tentativas += 1
                print("Limite exedido. Aguardando 60 segundos para tentar novamente...")
                time.sleep(60) 

        pub.setAvaliacao(avaliacao)

    return filtrados
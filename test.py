from spiders.youtube.youtube_lib import *
from entidades.Monitoramento import Monitoramento
from libs.navigator import Navigator

monitoramento = Monitoramento(1, 'test', 'prefeito zito duque de caxias', 'zito', 1,1)

navigator = Navigator('https://youtube.com/')

search(navigator, monitoramento.getPesquisa())

lista = get_list_publish(navigator)
print(lista[0].getTitulo())
print(lista[0].getData())

navigator.sleep()

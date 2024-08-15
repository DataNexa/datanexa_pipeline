from libs.request import get,post


req = post('/monitoramento/fila_list', { "client_id":1 })

print(req.body)
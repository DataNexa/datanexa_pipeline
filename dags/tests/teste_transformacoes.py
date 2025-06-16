from _dags.tasks.transformations.google.task_transform_processed_google import transform_processed_google
from services.API.APIGPT import chat
from libs.FileManager import read

import json

with open("arquivo.raw.google.json", "r") as f:
    file = json.load(f)

item = file.get("items", [])[0] if file.get("items") else {}

if not item:
    raise ValueError("Nenhum item encontrado no arquivo JSON.")

resposta = chat(item)

print(resposta)

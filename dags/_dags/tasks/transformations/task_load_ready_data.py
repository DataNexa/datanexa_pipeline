from libs.FileManager import FileManager, FileType, LocalFile, list_files, read
from services.API.APIDatanexa import APIDatanexa
from libs.Publish import Publish

def load_ready_data():

    arquivos = list_files(
        file_type=FileType.raw,
        local=LocalFile.google,
    )
    
    for arquivo in arquivos:

        objs:list = read(
            file_type=FileType.ready,
            filename=arquivo
        )

        publishs = []
        client_id = 0
        for obj in objs:
            if client_id == 0:
                client_id = obj["client_id"]
            obj['temImagem'] = obj['temImagem'] == 1
            obj['temVideo'] = obj['temVideo'] == 1
            publishs.append(Publish.create_by_dict(obj).to_dict())
        
        resp = APIDatanexa().post(f"/publicacoes/createMany?client_id={client_id}", publishs)

import logging

class MonitoramentoMetadata:

    id = None
    client_id = None

    def __init__(self, monitoramento:dict):
        self.id = monitoramento.get("id", None) 
        self.client_id = monitoramento.get("cliente_id", None)
        if self.id is None:
            raise ValueError("Campo 'id' ausente no monitoramento.")
        if self.client_id is None:
            raise ValueError("Campo 'client_id' ausente no monitoramento.")

    def add_monitoramento_metadata(self, object: dict):
        object['monitoramento'] = {
            "id": self.id,
            "client_id": self.client_id
        }
        return object
    

def add_metadata(monitoramento: dict, object: dict):
    logging.info("Adicionando Metadata ao Objeto")
    logging.info(monitoramento)
    try:
        metadata = MonitoramentoMetadata(monitoramento)
        return metadata.add_monitoramento_metadata(object)
    except ValueError as e:
        logging.error(f"Erro ao tentar adicionar metadata: {e}")
        return False

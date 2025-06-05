

class MonitoramentoMetadata:

    def __init__(self, monitoramento):
        self.id = monitoramento.get("id", None) 
        self.client_id = monitoramento.get("client_id", None)
        if self.id is None or self.client_id is None:
            raise ValueError("Monitoramento ID is required.")

    def add_monitoramento_metadata(self, object: dict):
        object['monitoramento'] = {
            "id": self.id,
            "client_id": self.client_id
        }
        return object
    

def add_metadata():
    """
    Decorator para adicionar metadados de monitoramento a um objeto 
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            monitoramento = kwargs.get('monitoramento', None)
            if not monitoramento:
                raise ValueError("Monitoramento é requerido.")
            metadata = MonitoramentoMetadata(monitoramento)
            result = func(*args, **kwargs)
            return metadata.add_monitoramento_metadata(result)
        return wrapper
    return decorator

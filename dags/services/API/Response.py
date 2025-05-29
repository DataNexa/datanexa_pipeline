
class Response:

    def __init__(self, status_code: int, body: dict|list, message: str):
        self._status_code = status_code
        self._body = body
        self._message = message

    def code(self):
        return self._status_code

    def body(self):
        return self._body

    def message(self):
        return self._message

    def __repr__(self):
        return f"Response(status_code={self.status_code}, data={self.data})"
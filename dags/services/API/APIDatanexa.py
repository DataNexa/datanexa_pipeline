from libs.Config import Config
import json
import requests
from services.API.Response import Response

class APIDatanexa:

    _session = ""
    _url = ""
    _token = ""


    def __init__(self):

        self.config = Config()
        self._url   = self.config.get("api_datanexa_url", "http://localhost:4000/")
        self._token = self.config.get("api_datanexa_token", "")
        
        if not self._url or not self._token:
            raise ValueError("API Datanexa URL ou Token não foram configurados.")
        
    def get(self, uri: str, data: dict = {}) -> Response:
        return self._request("get", uri, data)

    def post(self, uri: str, data: dict|list = {}) -> Response:
        return self._request("post", uri, data)


    def _ensure_session(self):
        if self._session == "":
            self._open_session()
    
    def _request(self, method: str, uri: str, data: dict = {}) -> Response:

        self._ensure_session()

        url = self._url + uri
        headers = {"Authorization": f"Bearer {self._session}"}

        if method.lower() == "get":
            response = requests.get(url, params=data, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return self._generate_response(response)
    

    def getSession(self) -> str:
        return self._session

    def _open_session(self):
        
        responseRequest = requests.post(f"{self._url}auth/openSessionUsingSecretToken", json={"secret_token": self._token})
        response = json.loads(responseRequest.text)

        if responseRequest.status_code == 200:
            self._session = response.get("body", "")
        else:
            raise ValueError(f"Falha ao tentar abrir sessão: {response.get('message', 'Unknown error')}")


    def _generate_response(self, responseRequest) -> Response:
        try:
            response_json = json.loads(responseRequest.text)
        except ValueError:
            response_json = {}

        body = response_json.get("body", {})
        message = response_json.get("message", "")

        return Response(responseRequest.status_code, body, message)
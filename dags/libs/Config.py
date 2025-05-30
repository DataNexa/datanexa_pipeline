import os
from dotenv import load_dotenv
from threading import Lock
import logging

class Config:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance._load()
            return cls._instance

    def _load(self):
        load_dotenv()
        self.google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.google_search_api_cx = os.getenv("GOOGLE_SEARCH_API_CX")
        self.api_datanexa_url = os.getenv("API_DATANEXA_URL")
        self.api_datanexa_token = os.getenv("API_DATANEXA_TOKEN")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

    def get(self, key, default=None):
        return getattr(self, key, default)
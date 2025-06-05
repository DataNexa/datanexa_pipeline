from enum import Enum
from pathlib import Path
import uuid
from datetime import datetime, timezone
import logging
import json

BASE_DIR = Path(__file__).parent

class FileType(str, Enum):
    processed = "processed"
    raw = "raw"
    ready = "ready"

class LocalFile(str, Enum):
    google = "google"
    instagram = "instagram"
    twitter = "twitter"
    youtube = "youtube"

class FileManager:


    def __init__(self, file_type: FileType, local: LocalFile, content: any, file_ext: str):

        self._type = file_type
        self._local = local
        self._content = content

        now = datetime.now(timezone.utc)
        self._filename = f"{now}.{uuid.uuid4().hex[:8]}.{local.value}.{file_type.value}.{file_ext}"
        if file_type.value == FileType.raw: 
            self._path = BASE_DIR / f"../data/{file_type.value}/{file_ext}/{local.value}/{self._filename}"
        else:
            self._path = BASE_DIR / f"../data/{file_type.value}/{local.value}/{self._filename}"

        logging.info("Arquivo gerado em FileManager:")
        logging.info(f"type={file_type}, local={local}, filename={self._filename}, path={self._path}")


    def save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(self._content, dict) or isinstance(self._content, list):  # JSON ou List
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._content, f, ensure_ascii=False, indent=2)
        else:  # texto comum
            self._path.write_text(str(self._content), encoding='utf-8')

        return self._path

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def path(self) -> Path:
        return self._path
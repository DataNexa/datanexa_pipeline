from enum import Enum
from pathlib import Path
import uuid
from datetime import datetime, timezone

class FileType(str, Enum):
    enriched = "enriched"
    processed = "processed"
    raw = "raw"
    ready = "ready"

class LocalFile(str, Enum):
    google = "google"
    instagram = "instagram"
    twitter = "twitter"
    youtube = "youtube"

class FileManager:

    def __init__(self, file_type: FileType, local: LocalFile, content: str, file_ext: str):
        self._type = file_type
        self._local = local
        self._content = content

        now = datetime.now(timezone.utc)
        self._filename = f"{now}_{uuid.uuid4().hex[:8]}.{local.value}.{file_type.value}.{file_ext}"
        if file_type.value == FileType.raw: 
            self._path = Path(f"dags/data/{file_type.value}/{file_ext}/{self._filename}").resolve()
        else:
            self._path = Path(f"dags/data/{file_type.value}/{local.value}/{self._filename}").resolve()

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(self._content, encoding='utf-8')

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def path(self) -> Path:
        return self._path
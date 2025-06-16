from enum import Enum
from pathlib import Path
import uuid
from datetime import datetime, timezone
import logging
import json

BASE_DIR = Path(__file__).parent

class FileType(str, Enum):
    processed = "processed"
    analise = "analise"
    raw = "raw"
    ready = "ready"

class LocalFile(str, Enum):
    google = "google"
    instagram = "instagram"
    twitter = "twitter"
    youtube = "youtube",
    none = ""

class FileManager:

    _path = ""
    _path_backup = ""


    def __init__(self, file_type: FileType, local: LocalFile, content: any, file_ext: str = "json") -> None:

        self._type = file_type
        self._local = f"/{local.value}" if local != LocalFile.none else ""
        self._content = content

        now  = datetime.now(timezone.utc)
        self._filename = f"{now}.{uuid.uuid4().hex[:8]}.{local.value}.{file_type.value}.{file_ext}"
        base_data = BASE_DIR / f"../data/"
        base_back = BASE_DIR / f"../backup/"

        if file_type.value == FileType.raw: 
            self._path = f"{base_data}{file_type.value}{local.value}/{file_ext}/{self._filename}"
            self._path_backup = f"{base_back}{file_type.value}{local.value}/{file_ext}/{self._filename}"
        elif file_type.value == FileType.ready or file_type.value == FileType.analise:
            self._path = f"{base_data}{file_type.value}/{self._filename}"
            self._path_backup = f"{base_back}{file_type.value}/{self._filename}"
        else:
            self._path = f"{base_data}{file_type.value}/{local.value}/{self._filename}"
            self._path_backup = f"{base_back}{file_type.value}/{local.value}/{self._filename}"

        logging.info("Arquivo gerado em FileManager:")
        logging.info(f"type={file_type}, local={local if local != "" else "root"}, filename={self._filename}, path={self._path}")


    def save(self, content: any = None) -> Path:
        
        if content is not None:
            self._content = content

        self._path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(self._content, dict) or isinstance(self._content, list):  # JSON ou List
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._content, f, ensure_ascii=False, indent=2)
            with open(self._path_backup, "w", encoding="utf-8") as f:
                json.dump(self._content, f, ensure_ascii=False, indent=2)
        else:
            self._path.write_text(str(self._content), encoding='utf-8')
            self._path_backup.write_text(str(self._content), encoding='utf-8')

        return self._path

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def path(self) -> Path:
        return self._path
    

def list_files(file_type: FileType, local: LocalFile|None = None, sufix:str = "") -> list[str]:
    
    if not local:
        local_values = ""
    else:
        local_values = f"/{local.value}"

    path = BASE_DIR / f"../data/{file_type.value}{local_values}{sufix}"
    
    if not path.exists():
        raise FileNotFoundError(f"Diretório {path} não encontrado.")

    return [f.name for f in path.glob("*") if f.is_file()]


def delete(file_type: FileType, local: LocalFile = None, filename: str = "") -> None:

    if not local:
        local_values = ""
    else:
        local_values = f"/{local.value}"

    path = BASE_DIR / f"../data/{file_type.value}{local_values}/{filename}"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo {filename} não encontrado em {path}")

    path.unlink()
    logging.info(f"Arquivo {filename} deletado com sucesso de {path}")


def read(file_type: FileType, filename: str, local: LocalFile|None = None ) -> any:

    if not local:
        local_values = ""
    else:
        local_values = f"/{local.value}"

    path = BASE_DIR / f"../data/{file_type.value}{local_values}/{filename}"
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo {filename} não encontrado em {path}")

    with open(path, "r", encoding="utf-8") as f:
        if path.suffix == '.json':
            return json.load(f)
        else:
            return f.read()
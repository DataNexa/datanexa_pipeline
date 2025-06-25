from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
from youtube_transcript_api.formatters import TextFormatter # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
import logging

from libs.FileManager import FileManager, FileType, LocalFile, read, list_files

# cria a transcrição do video e adiciona ao raw como obj "{video_id}.transcrito.obj.json"

def get_limited_transcript(video_id: str, max_chars: int = 12000) -> str:

    try:

        logging.info(f"Obtendo transcrição para o vídeo ID: {video_id}")

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])

        logging.info(f"Transcrição obtida... splitando em blocos de {max_chars} caracteres")

        full_text = ""

        for item in transcript_list:
            full_text += item['text'].replace('\n', '  ').strip()

        return full_text[:max_chars] if len(full_text) > max_chars else full_text

    except Exception as e:
        logging.error(f"Erro ao obter transcrição: {e}")
        return ""
    

def get_transcription_and_save():

    files = list_files(
        file_type=FileType.raw,
        local=LocalFile.youtube,
        sufix="/json"
    )

    logging.info(f"Arquivos encontrados: {files}")

    for file in files:
        if not file.endswith("raw.json"):
            continue

        try:
            obj = read(
                file_type=FileType.raw,
                local=LocalFile.youtube,
                filename=f"json/{file}",
            )

            relevancia = obj.get('metadata', {}).get('relevancia', 0)
            monitoramento = obj.get('monitoramento', {})
            if not monitoramento:
                raise Exception("Monitoramento não foi configurado no arquivo bruto para processamento")
            
            items = obj.get('items', [])
            i = 1
            for item in items:
                video_id = item.get('id', {}).get('videoId', '')
                if not video_id:
                    logging.error(f"ID do vídeo não encontrado no item: {item}")
                    continue

                item['video_id'] = video_id

                transcription = get_limited_transcript(video_id)

                if transcription:

                    item['texto'] = transcription
                    item['relevancia'] = relevancia / i
                    item['monitoramento'] = monitoramento
                    item['youtube_api_key'] = obj.get('youtube_api_key', '')

                    FileManager(
                        file_type=FileType.processed,
                        local=LocalFile.youtube,
                        content=item,
                        file_ext="transcrito.obj.json"
                    ).save()
                    i += 1

        except Exception as e:
            logging.error(f"Erro ao ler arquivo {file}: {e}")
            continue



def create_task_transform_transcription_data_youtube(dag):
    
    return PythonOperator(
        task_id='task_transform_transcription_data_youtube',
        python_callable=get_transcription_and_save,
        dag=dag
    )
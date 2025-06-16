from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
from youtube_transcript_api.formatters import TextFormatter # type: ignore

from libs.FileManager import FileManager, FileType, LocalFile, read, list_files

# cria a transcrição do video e adiciona ao raw como obj "{video_id}.transcrito.obj.json"

def get_limited_transcript(video_id: str, max_chars: int = 12000) -> str:

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR'])

        formatter = TextFormatter()
        full_text = formatter.format_transcript(transcript_list)
        
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars].rsplit('\n', 1)[0]  # Corta e tenta evitar quebra no meio de uma linha

        return full_text

    except Exception as e:
        print(f"Erro ao obter transcrição: {e}")
        return ""
    

def get_transcription_and_save():

    files = list_files(
        file_type=FileType.raw,
        local=LocalFile.youtube
    )

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
                    print(f"ID do vídeo não encontrado no item: {item}")
                    continue

                item['video_id'] = video_id

                transcription = get_limited_transcript(video_id)

                if transcription:

                    item['texto'] = transcription
                    item['relevancia'] = relevancia / i
                    item['monitoramento'] = monitoramento

                    FileManager(
                        file_type=FileType.processed,
                        local=LocalFile.youtube,
                        content=item,
                        file_ext="transcrito.obj.json"
                    ).save()
                    i += 1

        except Exception as e:
            print(f"Erro ao ler arquivo {file}: {e}")
            continue


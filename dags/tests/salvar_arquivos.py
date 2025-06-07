import libs.FileManager as FileManager

FileManager.FileManager(
    file_type=FileManager.FileType.enriched,
    local=FileManager.LocalFile.google,
    content="Hello, World!",
    file_ext="txt"
).save()

FileManager.FileManager(
    file_type=FileManager.FileType.processed,
    local=FileManager.LocalFile.instagram,
    content="{\"key\": \"value\"}",
    file_ext="json"
).save()

FileManager.FileManager(
    file_type=FileManager.FileType.raw,
    local=FileManager.LocalFile.twitter,
    content="<html><body>Hello, Twitter!</body></html>",
    file_ext="html"
).save()

FileManager.FileManager(
    file_type=FileManager.FileType.raw,
    local=FileManager.LocalFile.twitter,
    content="{\"tweet\": \"This is a sample tweet.\"}",
    file_ext="json"
).save()

FileManager.FileManager(
    file_type=FileManager.FileType.ready,
    local=FileManager.LocalFile.youtube,
    content="{\"video_id\": \"12345\", \"title\": \"Sample Video\"}",
    file_ext="json"
).save()
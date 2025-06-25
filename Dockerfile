FROM apache/airflow:3.0.1

USER airflow

# Instala youtube-transcript-api
RUN pip install --no-cache-dir youtube-transcript-api

USER airflow
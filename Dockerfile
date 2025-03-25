# Use a imagem oficial do Apache Airflow
FROM apache/airflow:2.7.1-python3.10

# Defina argumentos opcionais
ARG AIRFLOW_USER_HOME=/usr/local/airflow

# Crie diretórios e defina permissões
USER root
RUN mkdir -p ${AIRFLOW_USER_HOME}/dags ${AIRFLOW_USER_HOME}/logs ${AIRFLOW_USER_HOME}/plugins \
    && chown -R airflow: ${AIRFLOW_USER_HOME}

# Troque para o usuário Airflow
USER airflow

# Copie os arquivos DAGs e plugins (opcional)
COPY dags/ ${AIRFLOW_USER_HOME}/dags/
COPY plugins/ ${AIRFLOW_USER_HOME}/plugins/
COPY config/ ${AIRFLOW_USER_HOME}/config/
COPY scripts/ ${AIRFLOW_USER_HOME}/scripts/
# Instale pacotes Python adicionais (se necessário)
RUN pip install --no-cache-dir pandas boto3

# Defina variáveis de ambiente
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME} \
    PYTHONPATH=${AIRFLOW_USER_HOME}:/usr/local/lib/python3.10/site-packages

# Exponha a porta padrão do Airflow Webserver
EXPOSE 8080

# Comando padrão para iniciar o Airflow Webserver
CMD ["airflow", "webserver"]
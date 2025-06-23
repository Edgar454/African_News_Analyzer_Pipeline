FROM bitnami/spark:3.5.5

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

COPY spark_jobs /opt/bitnami/spark/jobs

USER 1001


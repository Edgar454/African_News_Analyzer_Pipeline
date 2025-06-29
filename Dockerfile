FROM apache/airflow:3.0.1

USER root

# Install OpenJDK 17 (needed for Spark)
RUN apt-get update && apt-get install -y openjdk-17-jdk curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME and PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Spark 3.5.5 (matches your other images)
ENV HADOOP_VERSION=3
RUN curl -fsSL https://dlcdn.apache.org/spark/spark-3.5.6/spark-3.5.6-bin-hadoop${HADOOP_VERSION}.tgz \
    | tar -xz -C /opt/ && \
    mv /opt/spark-3.5.6-bin-hadoop${HADOOP_VERSION} /opt/spark

# Set Spark env
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

USER airflow

# Install Airflow with Spark provider (pin version via ARG is good)
ARG AIRFLOW_VERSION=3.0.1
RUN pip install "apache-airflow[apache-spark]==${AIRFLOW_VERSION}"

# Install extra python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN python3 -m spacy download fr_core_news_sm
RUN python3 -m spacy download en_core_web_sm

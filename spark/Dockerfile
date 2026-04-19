FROM apache/spark:4.0.2

USER spark
# Set writable home and temp directories
ENV HOME=/tmp
ENV TMPDIR=/tmp

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


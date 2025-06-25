# --- Stage 1: Builder ---
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libffi-dev python3-dev libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt


# --- Stage 2: Runtime ---
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev libssl-dev\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app
COPY --from=builder /app/.venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

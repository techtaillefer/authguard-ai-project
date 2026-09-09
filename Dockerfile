FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts

RUN python -m pip install --no-cache-dir . \
    && mkdir -p data models \
    && python scripts/generate_data.py --rows 5000 --anomalies 250 \
    && python scripts/train.py

EXPOSE 8000
CMD ["uvicorn", "authguard.api:app", "--host", "0.0.0.0", "--port", "8000"]

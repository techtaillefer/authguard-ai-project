# AuthGuard AI

> AI-powered authentication anomaly detection for defensive cybersecurity.

![Focus](https://img.shields.io/badge/Focus-AI%20Cybersecurity-purple)
![ML](https://img.shields.io/badge/ML-Anomaly%20Detection-blue)
![Model](https://img.shields.io/badge/Model-Isolation%20Forest-green)
![API](https://img.shields.io/badge/API-FastAPI-009688)

![Python](https://img.shields.io/badge/Python-3.12-3776AB)
![Testing](https://img.shields.io/badge/Testing-pytest-green)
![Container](https://img.shields.io/badge/Container-Docker-2496ED)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)

![Security](https://img.shields.io/badge/Security-CodeQL-red)
![Dependencies](https://img.shields.io/badge/Dependencies-pip--audit-orange)
![Updates](https://img.shields.io/badge/Updates-Dependabot-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

AuthGuard AI is a defensive machine-learning demo that detects anomalous authentication events. It uses synthetic telemetry so the repository can be developed and tested without exposing real user or security logs.

## Architecture

1. Generate synthetic authentication events.
2. Engineer numeric features.
3. Train an Isolation Forest on normal baseline events.
4. Evaluate against held-out synthetic anomaly labels.
5. Serve scores through FastAPI.

The `context_flags` returned by the API are transparent rule-based indicators for analyst context; they are not explanations of the model's internal decision.

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python scripts/generate_data.py
python scripts/train.py
uvicorn authguard.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Test

```bash
ruff check .
ruff format --check .
pytest --cov=authguard --cov-report=term-missing
pip-audit
```

## Example score request

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H 'Content-Type: application/json' \
  -d '{
    "hour": 2,
    "failed_attempts": 8,
    "geo_distance_km": 5400,
    "device_trust_score": 0.12,
    "new_device": true,
    "impossible_travel": true,
    "ip_reputation_score": 10,
    "success": false
  }'
```

## Docker

```bash
docker build -t authguard-ai:local .
docker run --rm -p 8000:8000 authguard-ai:local
```

## Security notes

- This is a detection and triage demo, not an autonomous blocking system.
- Use only authorized telemetry.
- Do not train on secrets, passwords, session tokens, or unnecessary personal data.
- Treat serialized model files as trusted artifacts; do not load untrusted Joblib/Pickle files.
- In production, add authentication, authorization, rate limiting, TLS, monitoring, and a controlled model registry.

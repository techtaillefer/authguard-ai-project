"""Model loading and scoring."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from authguard.features import engineer_features

DEFAULT_MODEL_PATH = "models/isolation_forest.joblib"


@lru_cache(maxsize=1)
def get_model_bundle() -> dict:
    """Load the trained model bundle once per process."""
    path = Path(os.getenv("AUTHGUARD_MODEL_PATH", DEFAULT_MODEL_PATH))
    if not path.exists():
        raise FileNotFoundError(
            f"Model not found at {path}. "
            "Run: python scripts/generate_data.py && python scripts/train.py"
        )
    return joblib.load(path)


def context_flags(event: dict) -> list[str]:
    """Return transparent rule-based context flags; these are not model explanations."""
    flags: list[str] = []
    if event["failed_attempts"] >= 5:
        flags.append("many_failed_attempts")
    if event["geo_distance_km"] >= 1000:
        flags.append("large_geo_distance")
    if event["device_trust_score"] <= 0.35:
        flags.append("low_device_trust")
    if event["new_device"]:
        flags.append("new_device")
    if event["impossible_travel"]:
        flags.append("impossible_travel")
    if event["ip_reputation_score"] <= 35:
        flags.append("low_ip_reputation")
    if not event["success"]:
        flags.append("login_failed")
    return flags


def score_event(event: dict) -> dict:
    """Score one raw authentication event."""
    bundle = get_model_bundle()
    pipeline = bundle["pipeline"]
    X = engineer_features(pd.DataFrame([event]))

    prediction = int(pipeline.predict(X)[0])
    decision = float(pipeline.decision_function(X)[0])

    return {
        "is_anomaly": prediction == -1,
        "anomaly_score": round(-decision, 6),
        "context_flags": context_flags(event),
        "model_version": bundle["metadata"]["project_version"],
    }

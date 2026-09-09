"""Feature engineering for authentication events."""

from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "hour_sin",
    "hour_cos",
    "failed_attempts",
    "geo_distance_log",
    "device_trust_score",
    "new_device",
    "impossible_travel",
    "ip_risk_score",
    "login_failed",
]

REQUIRED_RAW_COLUMNS = [
    "hour",
    "failed_attempts",
    "geo_distance_km",
    "device_trust_score",
    "new_device",
    "impossible_travel",
    "ip_reputation_score",
    "success",
]


def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert raw authentication-event fields into model-ready numeric features."""
    missing = sorted(set(REQUIRED_RAW_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    result = pd.DataFrame(index=frame.index)
    hour = frame["hour"].astype(float)
    result["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    result["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    result["failed_attempts"] = frame["failed_attempts"].astype(float)
    result["geo_distance_log"] = np.log1p(frame["geo_distance_km"].astype(float))
    result["device_trust_score"] = frame["device_trust_score"].astype(float)
    result["new_device"] = frame["new_device"].astype(int)
    result["impossible_travel"] = frame["impossible_travel"].astype(int)
    result["ip_risk_score"] = 1.0 - (frame["ip_reputation_score"].astype(float) / 100.0)
    result["login_failed"] = 1 - frame["success"].astype(int)
    return result[FEATURE_COLUMNS]

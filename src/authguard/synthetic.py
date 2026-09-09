"""Synthetic authentication-event generator for safe local experimentation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd


def generate_events(
    normal_rows: int = 5000, anomaly_rows: int = 250, seed: int = 42
) -> pd.DataFrame:
    """Generate labeled synthetic login telemetry.

    The labels are used only for evaluation. The anomaly detector is trained on
    normal baseline events.
    """
    rng = np.random.default_rng(seed)

    normal = pd.DataFrame(
        {
            "hour": rng.integers(6, 23, normal_rows),
            "failed_attempts": np.clip(rng.poisson(0.25, normal_rows), 0, 3),
            "geo_distance_km": np.clip(rng.gamma(2.0, 35.0, normal_rows), 0, 500),
            "device_trust_score": rng.beta(9.0, 2.0, normal_rows),
            "new_device": rng.random(normal_rows) < 0.05,
            "impossible_travel": np.zeros(normal_rows, dtype=bool),
            "ip_reputation_score": np.clip(rng.normal(86, 8, normal_rows), 45, 100),
            "success": rng.random(normal_rows) < 0.985,
            "is_anomaly": np.zeros(normal_rows, dtype=int),
        }
    )

    anomaly = pd.DataFrame(
        {
            "hour": rng.integers(0, 24, anomaly_rows),
            "failed_attempts": rng.integers(3, 13, anomaly_rows),
            "geo_distance_km": rng.uniform(750, 12000, anomaly_rows),
            "device_trust_score": rng.uniform(0.02, 0.45, anomaly_rows),
            "new_device": rng.random(anomaly_rows) < 0.80,
            "impossible_travel": rng.random(anomaly_rows) < 0.60,
            "ip_reputation_score": rng.uniform(0, 38, anomaly_rows),
            "success": rng.random(anomaly_rows) < 0.25,
            "is_anomaly": np.ones(anomaly_rows, dtype=int),
        }
    )

    frame = pd.concat([normal, anomaly], ignore_index=True)
    frame = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    start = datetime(2026, 1, 1, tzinfo=UTC)
    offsets = rng.integers(0, 60 * 24 * 90, len(frame))
    frame.insert(0, "event_id", [f"evt-{i:06d}" for i in range(len(frame))])
    frame.insert(
        1,
        "timestamp",
        [(start + timedelta(minutes=int(offset))).isoformat() for offset in offsets],
    )
    return frame

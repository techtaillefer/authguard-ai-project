"""Training and evaluation logic."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from authguard import __version__
from authguard.features import FEATURE_COLUMNS, engineer_features


def train_model(
    data_path: str | Path,
    model_path: str | Path,
    metadata_path: str | Path,
    random_state: int = 42,
) -> dict:
    """Train on normal baseline events and evaluate against held-out synthetic labels."""
    data_path = Path(data_path)
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)

    frame = pd.read_csv(data_path)
    if "is_anomaly" not in frame.columns:
        raise ValueError("Training data must include the is_anomaly evaluation label")

    X = engineer_features(frame)
    y = frame["is_anomaly"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=random_state,
        stratify=y,
    )

    baseline = X_train[y_train == 0]

    pipeline = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "model",
                IsolationForest(
                    n_estimators=250,
                    contamination=0.03,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    pipeline.fit(baseline)

    predicted = (pipeline.predict(X_test) == -1).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        predicted,
        average="binary",
        zero_division=0,
    )

    metadata = {
        "project_version": __version__,
        "trained_at_utc": datetime.now(UTC).isoformat(),
        "training_rows": int(len(baseline)),
        "test_rows": int(len(X_test)),
        "feature_columns": FEATURE_COLUMNS,
        "metrics": {
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1": round(float(f1), 4),
        },
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "metadata": metadata}, model_path)
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata

import numpy as np
import pandas as pd

from authguard.features import FEATURE_COLUMNS, engineer_features


def test_engineer_features_has_expected_shape_and_no_nan() -> None:
    raw = pd.DataFrame(
        [
            {
                "hour": 23,
                "failed_attempts": 2,
                "geo_distance_km": 12.5,
                "device_trust_score": 0.9,
                "new_device": False,
                "impossible_travel": False,
                "ip_reputation_score": 92,
                "success": True,
            }
        ]
    )

    result = engineer_features(raw)

    assert list(result.columns) == FEATURE_COLUMNS
    assert result.shape == (1, len(FEATURE_COLUMNS))
    assert np.isfinite(result.to_numpy()).all()

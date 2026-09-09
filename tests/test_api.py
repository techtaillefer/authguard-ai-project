from fastapi.testclient import TestClient

import authguard.api as api_module


client = TestClient(api_module.app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_score(monkeypatch) -> None:
    monkeypatch.setattr(
        api_module,
        "score_event",
        lambda event: {
            "is_anomaly": True,
            "anomaly_score": 0.123,
            "context_flags": ["new_device"],
            "model_version": "0.1.0",
        },
    )

    response = client.post(
        "/score",
        json={
            "hour": 2,
            "failed_attempts": 7,
            "geo_distance_km": 4200,
            "device_trust_score": 0.15,
            "new_device": True,
            "impossible_travel": True,
            "ip_reputation_score": 12,
            "success": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["is_anomaly"] is True

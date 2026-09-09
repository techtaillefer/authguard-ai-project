from authguard.synthetic import generate_events
from authguard.training import train_model


def test_training_creates_model_and_metadata(tmp_path) -> None:
    data_path = tmp_path / "events.csv"
    model_path = tmp_path / "model.joblib"
    metadata_path = tmp_path / "metadata.json"

    generate_events(normal_rows=600, anomaly_rows=60, seed=7).to_csv(data_path, index=False)
    metadata = train_model(data_path, model_path, metadata_path, random_state=7)

    assert model_path.exists()
    assert metadata_path.exists()
    assert metadata["metrics"]["recall"] >= 0.8
    assert metadata["metrics"]["precision"] >= 0.5

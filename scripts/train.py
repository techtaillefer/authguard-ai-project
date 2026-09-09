#!/usr/bin/env python3
"""Train AuthGuard's anomaly detector."""

from __future__ import annotations

import argparse
import json

from authguard.training import train_model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/auth_events.csv")
    parser.add_argument("--model", default="models/isolation_forest.joblib")
    parser.add_argument("--metadata", default="models/metadata.json")
    args = parser.parse_args()

    metadata = train_model(args.data, args.model, args.metadata)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

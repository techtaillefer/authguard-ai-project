#!/usr/bin/env python3
"""Generate synthetic authentication data."""

from __future__ import annotations

import argparse
from pathlib import Path

from authguard.synthetic import generate_events


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=5000, help="Normal event count")
    parser.add_argument("--anomalies", type=int, default=250, help="Synthetic anomaly count")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/auth_events.csv")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame = generate_events(args.rows, args.anomalies, args.seed)
    frame.to_csv(output, index=False)
    print(f"Wrote {len(frame)} rows to {output}")


if __name__ == "__main__":
    main()

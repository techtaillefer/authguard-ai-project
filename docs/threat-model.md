# Threat model

## Assets

- Authentication telemetry
- Trained model artifacts
- API availability and integrity
- CI/CD credentials and GitHub tokens
- Model evaluation history

## Trust boundaries

1. Telemetry enters the data pipeline.
2. Training creates a serialized model artifact.
3. The API loads the artifact and accepts scoring requests.
4. GitHub Actions executes repository code and dependency tooling.

## Main threats and controls

| Threat | Example | Control |
| --- | --- | --- |
| Data poisoning | Malicious or corrupt events distort the baseline | Validate schemas, use approved data sources, track dataset versions, review drift |
| Artifact substitution | An attacker replaces the model file | Store artifacts in a controlled registry, verify hashes/signatures, restrict write access |
| Sensitive-data leakage | Raw logs contain PII or secrets | Minimize fields, redact secrets, define retention, restrict access |
| API abuse | High-volume requests exhaust resources | Authentication, authorization, rate limits, quotas, monitoring |
| Dependency compromise | Vulnerable or malicious package enters build | Pin/lock dependencies, Dependabot, pip-audit, review updates |
| CI token abuse | Workflow gets excessive repository permissions | Explicit least-privilege `permissions`, protected branches, review workflow changes |
| Model drift | Normal behavior changes over time | Monitor score distributions, evaluate on fresh labeled samples, retrain under change control |
| False positives | Legitimate users are flagged | Human review; do not use this demo as an autonomous blocking system |

## Non-goals

This project does not exploit systems, harvest credentials, perform intrusion, or automatically block accounts.

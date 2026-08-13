# Add service account key rotation evidence gate

<!-- daily-pr-task: service-account-key-rotation-evidence-gate -->

Automation credentials require rotation evidence without exposing the credential itself. This offline gate validates key metadata: unique service accounts, opaque key identifiers, timezone-aware rotation and expiry timestamps, and a positive rotation age within policy. It never reads or outputs key material.

## Portfolio Value

Demonstrates credential hygiene for operational automation while keeping all secret values out of repository data and logs.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fresh unexpired key metadata passes while empty input, duplicate accounts, missing identifiers, stale rotations, expired keys, malformed timestamps, and invalid policy values fail.

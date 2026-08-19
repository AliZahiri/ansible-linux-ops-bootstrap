# Add backup key rotation evidence gate

<!-- daily-pr-task: backup-key-rotation-evidence-gate -->

This offline evidence gate validates an active key identifier, backup scope, explicit rotation verification, timezone-aware rotation and expiry timestamps, and a bounded rotation age. It never reads or stores key material, vault passwords, or production credentials.

## Portfolio Value

Extends backup recovery readiness with auditable encryption-key lifecycle evidence.

## Validation

Run python3 -m unittest discover -s tests. Tests cover valid recent evidence, missing identifiers and scope, inactive or unverified keys, stale rotation, expired keys, and invalid policy or clock values.

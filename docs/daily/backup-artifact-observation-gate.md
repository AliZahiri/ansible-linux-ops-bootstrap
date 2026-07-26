# Add backup artifact observation gate

<!-- daily-pr-task: backup-artifact-observation-gate -->

A syntactically valid backup manifest does not prove that the observed artifact matches it. This metadata-only gate composes the existing manifest contract with independently observed byte size and SHA-256 values, reports manifest and observation failures separately, and rejects size or digest mismatches without opening the backup or exposing its contents.

## Portfolio Value

Extends the backup metadata contract into deterministic artifact identity evidence by comparing independent size and checksum observations.

## Validation

Run `python3 -m unittest discover -s tests` and confirm matching observations pass while invalid manifests, boolean/non-positive sizes, incomplete digests, and size or checksum mismatches fail independently.

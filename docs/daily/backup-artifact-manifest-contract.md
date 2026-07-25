# Add backup artifact manifest contract

<!-- daily-pr-task: backup-artifact-manifest-contract -->

Backup and restore checks need a stable metadata contract before they can verify an artifact. This validator requires a bounded backup identifier, a path-free artifact name, a timezone-aware creation timestamp, a positive byte size, and a complete SHA-256 digest. It validates metadata only, never opens the backup artifact, and returns field-level violations without exposing backup contents.

## Portfolio Value

Adds a deterministic, content-safe metadata boundary that later checksum, retention, and restore automation can consume consistently.

## Validation

Run `python3 -m unittest discover -s tests` and confirm complete manifests pass while unsafe identifiers, path-bearing names, naive timestamps, non-positive sizes, and incomplete digests fail.

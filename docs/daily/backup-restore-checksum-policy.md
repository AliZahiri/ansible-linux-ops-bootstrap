# Add backup restore checksum policy

<!-- daily-pr-task: backup-restore-checksum-policy -->

Restore operations should verify a recorded checksum before applying a backup artifact. The helper is intentionally small, avoids credentials, and gives operators a clear failure when an artifact changes unexpectedly.

## Portfolio Value

Strengthens restore safety with an explicit integrity check before backup data is used.

## Validation

Run `python3 -m unittest discover -s tests` and confirm the checksum helper requires both artifact and checksum file.

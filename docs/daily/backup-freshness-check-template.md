# Add backup freshness check template

<!-- daily-pr-task: backup-freshness-check-template -->

A successful backup is not enough when the last artifact is stale. This template exposes a lightweight freshness check that monitoring can run without reading backup credentials or parsing application logs.

## Portfolio Value

Adds a monitorable safeguard for stale backups and makes operational readiness visible in the repository.

## Validation

Run `python3 -m unittest discover -s tests` and confirm the freshness script requires an artifact and avoids credentials.

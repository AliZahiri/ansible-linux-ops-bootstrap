# Add backup healthcheck hook template

<!-- daily-pr-task: backup-healthcheck-hook -->

Backup jobs should emit a lightweight health signal after a successful run. This gives monitoring a simple way to detect stale or failing backups without reading large log files.

Hook behavior:

- fail when backup artifact path is missing
- write a timestamped status file
- include backup artifact name
- keep output free of credentials

## Portfolio Value

Strengthens backup operational readiness with a monitorable success signal.

## Validation

Run `python3 -m unittest discover -s tests` and confirm the hook requires an artifact and avoids credentials.

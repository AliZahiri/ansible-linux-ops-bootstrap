# Add backup artifact permission policy

<!-- daily-pr-task: backup-artifact-permission-policy -->

Backup artifacts should be created with restrictive ownership and permissions from the start. The bootstrap role can provide a small helper that verifies the backup directory, artifact mode, and group are explicit without placing credentials in scripts.

Policy controls:

- backup directory mode is 0750
- backup artifacts use mode 0640
- owner and group are configurable
- script fails when artifact path is missing

## Portfolio Value

Adds a practical hardening control for backup operations and least-privilege file handling.

## Validation

Run `python3 -m unittest discover -s tests` and confirm generated backup artifacts use restrictive permissions.

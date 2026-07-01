# Add backup restore drill policy

<!-- daily-pr-task: backup-restore-drill-policy -->

Backup restore drill policy should verify that backup artifacts can be restored into a safe target. Operators should test restore behavior before relying on backups in incidents.

Drill inputs:

- backup manifest path
- restore target
- dry-run flag
- operator

## Portfolio Value

Shows server bootstrap includes recoverability checks instead of backup creation alone.

## Validation

Run the unit test and confirm the restore drill script validates target and manifest inputs.

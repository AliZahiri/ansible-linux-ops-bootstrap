# Add backup retention policy

<!-- daily-pr-task: backup-retention-policy -->

Backup automation should include retention policy so storage usage and recovery expectations are explicit. Short-term daily backups and longer monthly retention should be documented separately.

Policy fields:

- daily retention days
- monthly retention months
- minimum restore points
- encrypted archive requirement

## Portfolio Value

Completes the backup story with retention controls that prevent unbounded storage growth.

## Validation

Run the unit test and confirm retention values are positive and ordered.

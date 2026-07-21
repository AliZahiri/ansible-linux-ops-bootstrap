# Add backup RPO policy validator

<!-- daily-pr-task: backup-rpo-policy-validator -->

A backup file can exist and still be too old to satisfy the recovery point objective. This validator compares timezone-aware last-success and observation timestamps against an explicit maximum age, rejects clock reversal, and operates on metadata only. It can be used by Ansible checks without reading backup contents or credentials.

## Portfolio Value

Turns backup freshness into an explicit recovery objective gate with deterministic timezone-aware behavior suitable for Linux operations automation.

## Validation

Run `python3 -m unittest discover -s tests` and confirm recent backups pass while stale, future, or timezone-naive metadata is rejected.

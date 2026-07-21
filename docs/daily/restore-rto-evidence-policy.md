# Add restore RTO evidence policy

<!-- daily-pr-task: restore-rto-evidence-policy -->

A successful restore drill should prove both integrity and completion within the recovery time objective. This policy validates the existing machine-readable drill evidence, requires checksum and application verification, and compares timezone-aware start and completion timestamps to a bounded duration. No production inventory or secret data is required.

## Portfolio Value

Connects restore drill evidence to a measurable recovery time objective while requiring integrity and application-level validation.

## Validation

Run `python3 -m unittest discover -s tests` and confirm slow, unverified, reversed, or timezone-invalid restore evidence fails the RTO policy.

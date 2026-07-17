# Add restore drill evidence template

<!-- daily-pr-task: restore-drill-evidence-template -->

A restore drill should produce machine-readable evidence that identifies the backup artifact, records checksum verification, captures the test window, and states whether application-level validation passed. The evidence contains operational metadata only and no credentials.

## Portfolio Value

Turns restore testing into auditable recovery evidence without exposing production secrets.

## Validation

Run `python3 -m unittest discover -s tests` and confirm the evidence template records integrity, timing, and application verification fields.

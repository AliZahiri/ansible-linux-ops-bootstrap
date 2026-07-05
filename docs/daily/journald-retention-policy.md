# Add journald retention policy

<!-- daily-pr-task: journald-retention-policy -->

journald retention policy should prevent unbounded log growth and keep enough history for incident response.

Policy fields:

- system max use
- max retention time
- compression enabled
- persistent storage

## Portfolio Value

Shows host bootstrap controls log growth while preserving incident evidence.

## Validation

Run the unit test and confirm journald retention and compression are templated.

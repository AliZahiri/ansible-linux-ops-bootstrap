# Add logrotate baseline policy

<!-- daily-pr-task: logrotate-baseline-policy -->

Log rotation should be installed alongside long-running services so disks do not fill silently. Baseline policy should define rotation frequency, retention, compression, and missing file behavior.

Policy fields:

- log path
- rotate count
- compression
- missingok behavior

## Portfolio Value

Shows host bootstrap includes disk hygiene for long-running services.

## Validation

Run the unit test and confirm rotation and compression are configured.

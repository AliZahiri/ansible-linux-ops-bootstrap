# Add systemd service policy

<!-- daily-pr-task: systemd-service-policy -->

Systemd units for platform services should include restart behavior, dependency ordering, and log visibility. This makes service recovery predictable after host changes.

Policy checks:

- restart policy
- restart delay
- wanted-by target
- environment file path

## Portfolio Value

Shows Linux bootstrap roles manage service reliability instead of only installing packages.

## Validation

Run the unit test and confirm restart policy is explicit.

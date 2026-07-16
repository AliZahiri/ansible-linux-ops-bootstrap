# Add systemd resource limit template

<!-- daily-pr-task: systemd-resource-limit-template -->

Service-level resource limits prevent one workload from exhausting a host during an incident. The template keeps memory and file descriptor limits configurable and visible in version control.

## Portfolio Value

Shows Linux operational hardening includes service isolation, not only host-level configuration.

## Validation

Run `python3 -m unittest discover -s tests` and confirm all three resource controls are present.

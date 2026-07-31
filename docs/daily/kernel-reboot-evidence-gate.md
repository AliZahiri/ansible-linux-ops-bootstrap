# Add kernel reboot evidence gate

<!-- daily-pr-task: kernel-reboot-evidence-gate -->

Installing security updates does not prove that a host is running the patched kernel. This metadata-only gate compares running and installed kernel releases, requires a reboot or an explicit approved deferral when they differ, and validates a bounded timezone-aware deferral deadline. It reads supplied evidence only and never contacts inventory or reboots a host.

## Portfolio Value

Closes the gap between package installation and effective kernel remediation by requiring current-kernel evidence or a bounded, auditable reboot deferral.

## Validation

Run `python3 -m unittest discover -s tests` and confirm current kernels and bounded approved deferrals pass while invalid releases, missing tickets, naive/expired/excessive deadlines, and invalid policy values fail.

# Add systemd resource-limit evidence gate

<!-- daily-pr-task: systemd-resource-limit-evidence-gate -->

A systemd resource-limit template is useful only when its applied values are verified on the managed host. This offline gate validates fresh systemctl-derived evidence for an active service: a safe unit name, positive memory and task limits, a sufficiently high file-descriptor ceiling, and an explicit configuration-read result. It evaluates supplied observations without connecting to a host.

## Portfolio Value

Turns systemd hardening from template intent into fresh, reviewable evidence that the resource boundaries expected by platform services are actually active.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fresh active service evidence passes while invalid units, inactive services, unread configuration, missing resource limits, low file descriptors, stale or naive timestamps, and invalid policy values fail.

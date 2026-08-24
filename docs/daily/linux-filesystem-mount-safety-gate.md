# Add Linux filesystem mount safety gate

<!-- daily-pr-task: linux-filesystem-mount-safety-gate -->

Filesystem hardening should be verified against declared mount evidence before a host is considered compliant. This offline gate requires a root mount, unique absolute targets, explicit filesystem types and options, and policy-driven options such as nodev, nosuid, or noexec for sensitive paths.

## Portfolio Value

Extends host hardening from configuration intent to deterministic mount-policy evidence without requiring a production inventory or privileged probe.

## Validation

Run python3 -m unittest discover -s tests and confirm missing root mounts, duplicate or relative targets, invalid types/options, and absent required hardening flags fail.

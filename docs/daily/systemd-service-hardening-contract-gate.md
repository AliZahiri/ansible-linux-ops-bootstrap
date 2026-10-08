# Add systemd service hardening contract gate

<!-- daily-pr-task: systemd-service-hardening-contract-gate -->

A service that restarts correctly can still expose an unnecessary host attack surface. This offline contract validates explicit systemd isolation directives before a unit template is promoted. The defaults are intentionally conservative and should be reviewed for compatibility with each workload; this gate validates declared settings and does not modify hosts.

## Portfolio Value

Adds a reviewable least-privilege contract for service units, complementing restart and resource controls with concrete host isolation requirements.

## Validation

Run python3 -m unittest discover -s tests and confirm required isolation directives and absolute writable paths pass while disabled or malformed settings fail.

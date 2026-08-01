# Add audit log forwarding evidence gate

<!-- daily-pr-task: audit-log-forwarding-evidence-gate -->

Installing auditd rules does not prove that security events leave the host or survive an upstream outage. This metadata-only gate requires an active forwarding service, authenticated TLS, a disk-backed queue, at least one destination, zero dropped events, and a fresh timezone-aware delivery observation. It never contacts inventory or stores destination credentials.

## Portfolio Value

Extends host hardening beyond local audit rules with deterministic evidence that security logs are securely forwarded, buffered, fresh, and not being dropped.

## Validation

Run `python3 -m unittest discover -s tests` and confirm active TLS-verified queued forwarding passes while inactive service, missing destinations, invalid counters, dropped events, stale/future/naive delivery timestamps, and invalid policies fail.

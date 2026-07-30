# Add systemd unit verification gate

<!-- daily-pr-task: systemd-unit-verification-gate -->

A successful Ansible task does not prove that a changed systemd unit was reloaded, enabled, active, and recently observed without restart churn. This metadata-only gate validates unit identity, daemon-reload evidence, enabled and active state, service result, bounded restart count, and a fresh timezone-aware observation. It never contacts systemd or managed inventory.

## Portfolio Value

Adds deterministic post-change evidence for stable systemd units so Ansible success is not confused with a healthy, enabled, freshly observed service.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fresh stable units pass while malformed names, missing reload/enabled/active evidence, failed results, restart churn, stale/future/naive observations, and invalid policy values fail.

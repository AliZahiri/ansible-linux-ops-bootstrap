# Add package manager lock readiness gate

<!-- daily-pr-task: package-manager-lock-readiness-gate -->

Ansible package tasks should not race apt, dpkg, or unattended-upgrades. This offline gate validates unique host evidence, fresh timezone-aware observations, explicit lock state, and complete owner metadata when a lock is held. It reports stale owners for operator review and never recommends deleting package-manager lock files.

## Portfolio Value

Adds safe preflight evidence for Ansible package operations so automation waits for package-manager owners instead of racing transactions or deleting locks.

## Validation

Run python3 -m unittest discover -s tests and confirm held locks, duplicate hosts, stale observations, missing owner metadata, stale owners, and invalid policy fail.

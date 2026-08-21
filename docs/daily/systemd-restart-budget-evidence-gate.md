# Add systemd restart budget evidence gate

<!-- daily-pr-task: systemd-restart-budget-evidence-gate -->

A service should not repeatedly restart unnoticed after automation changes. This offline evidence gate validates a positive restart budget, an observed count within the budget, an active unit, a bounded observation window, and a timezone-aware observation timestamp.

## Portfolio Value

Adds measurable post-change restart evidence so systemd automation can surface restart storms instead of only declaring configuration success.

## Validation

Run `python3 -m unittest discover -s tests` and confirm only active services with bounded restarts and complete observation evidence pass.

# Add Ansible check-mode change budget gate

<!-- daily-pr-task: ansible-check-mode-change-budget-gate -->

A check-mode run should provide bounded, reviewable change evidence before production execution. This offline gate requires a positive host count, zero failed or unreachable hosts, changes within policy, and a timezone-aware observation timestamp.

## Portfolio Value

Adds a measurable pre-execution safety control that complements idempotency reporting and prevents unexpectedly broad Ansible changes.

## Validation

Run python3 -m unittest discover -s tests and confirm failed, unreachable, oversized, malformed, or naive-timestamped check-mode reports fail.

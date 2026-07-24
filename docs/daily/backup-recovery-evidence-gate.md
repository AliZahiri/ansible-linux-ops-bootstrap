# Add backup recovery evidence gate

<!-- daily-pr-task: backup-recovery-evidence-gate -->

Recovery readiness requires both a recent successful backup and a verified restore completed within RTO. This aggregate evidence gate connects the existing RPO and restore policies, requires a stable backup identifier, and returns machine-readable violations without inspecting backup contents.

## Portfolio Value

Turns backup freshness and restore-drill evidence into one measurable recovery readiness decision.

## Validation

Run `python3 -m unittest discover -s tests` and confirm RPO, RTO, identity, checksum, and application verification failures remain visible.

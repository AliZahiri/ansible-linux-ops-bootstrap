# Add backup restore point diversity gate

<!-- daily-pr-task: backup-restore-point-diversity-gate -->

A backup policy needs more than one recent artifact: restore points should be distinct and span the stated recovery window. This offline gate validates unique backup identifiers, immutable digests, timezone-aware timestamps, and a minimum number of artifacts within a bounded age budget.

## Portfolio Value

Adds a measurable recovery-point diversity check to backup evidence, making it harder for one reused or stale artifact to be mistaken for restore readiness.

## Validation

Run `python3 -m unittest discover -s tests` and confirm distinct recent restore points pass while sparse, duplicate, invalid-digest, stale, malformed, and invalid-policy records fail.

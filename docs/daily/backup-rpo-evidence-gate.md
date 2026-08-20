# Add backup RPO evidence gate

<!-- daily-pr-task: backup-rpo-evidence-gate -->

Backup freshness should be measured against an explicit recovery point objective (RPO), not a vague recent-success signal. This offline gate checks a declared positive RPO, a non-negative observed backup age within that objective, and a timezone-aware verification timestamp. It validates evidence only and never accesses backup storage.

## Portfolio Value

Turns backup freshness into an auditable service objective that complements restore and retention evidence.

## Validation

Run `python3 -m unittest discover -s tests` and confirm only a verified backup within a positive RPO passes.

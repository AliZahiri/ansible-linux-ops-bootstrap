# Add file integrity monitor evidence gate

<!-- daily-pr-task: file-integrity-monitor-evidence-gate -->

Installing a file-integrity monitor does not prove its baseline exists or that scans still run. This offline gate validates active scheduling, an initialized baseline digest, a fresh successful scan, and a bounded count of explicitly reviewed critical-file changes. It consumes summary evidence only and never collects file content.

## Portfolio Value

Turns file-integrity tooling into auditable operational evidence and detects missing baselines, stopped schedules, stale scans, and unreviewed critical changes.

## Validation

Run python3 -m unittest discover -s tests and confirm a fresh successful scheduled scan with a valid baseline digest and reviewed change budget passes.

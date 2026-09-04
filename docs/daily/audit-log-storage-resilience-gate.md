# Add audit log storage resilience gate

<!-- daily-pr-task: audit-log-storage-resilience-gate -->

Audit rules provide little forensic value if disk pressure silently stops logging or overwrites evidence. This offline configuration gate validates conservative auditd space thresholds, actionable low-space and full-disk responses, retained log rotation, and a minimum free-space reserve. It validates declared effective settings without collecting log contents.

## Portfolio Value

Adds a failure-mode control for audit evidence loss under disk pressure and demonstrates conservative, reviewable auditd storage policy.

## Validation

Run python3 -m unittest discover -s tests and confirm auditd storage requires sufficient reserve, alerting and containment actions, rotation, and retained logs.

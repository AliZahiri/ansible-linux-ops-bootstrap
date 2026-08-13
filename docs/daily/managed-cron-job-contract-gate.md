# Add managed cron job contract gate

<!-- daily-pr-task: managed-cron-job-contract-gate -->

Scheduled operational jobs should have ownership, bounded cadence, and observable output. This offline gate validates cron metadata: unique names, five-field schedules without wildcard-only cadence, explicit non-root owner, and a log destination under /var/log. It evaluates declared Ansible job data without scheduling anything.

## Portfolio Value

Adds operational discipline for recurring host automation by making schedule, privilege, ownership, and observability reviewable.

## Validation

Run `python3 -m unittest discover -s tests` and confirm owned bounded observable jobs pass while empty input, duplicate names, wildcard-only schedules, root ownership, and unsafe log paths fail.

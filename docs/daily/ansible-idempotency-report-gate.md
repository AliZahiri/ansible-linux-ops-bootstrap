# Add Ansible idempotency report gate

<!-- daily-pr-task: ansible-idempotency-report-gate -->

An idempotency claim should be backed by two successful runs against the same host set. This deterministic gate accepts Ansible recap metadata, allows expected changes during the first run, and requires zero changes during the verification run. It rejects missing hosts, failed or unreachable results, negative or non-integer counters, and host-set drift without contacting managed systems or reading credentials.

## Portfolio Value

Turns Ansible idempotency from a documentation claim into a machine-readable two-run evidence gate with explicit failure semantics.

## Validation

Run `python3 -m unittest discover -s tests` and confirm first-run changes are allowed while verification changes, failures, unreachable hosts, invalid counters, and host-set drift fail.

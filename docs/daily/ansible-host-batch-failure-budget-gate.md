# Add Ansible host batch failure budget gate

<!-- daily-pr-task: ansible-host-batch-failure-budget-gate -->

Rolling Ansible changes should stop when a host batch exceeds an explicit failure budget. This offline gate validates a named batch, positive host counts, bounded failed and unreachable hosts, and timezone-aware completion evidence.

## Portfolio Value

Turns Ansible rolling-update failure tolerance into deterministic evidence that can stop later batches before broad host impact.

## Validation

Run python3 -m unittest discover -s tests and confirm malformed or over-budget batch summaries fail deterministically.

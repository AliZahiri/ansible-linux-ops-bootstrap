# Add Ansible playbook change-scope gate

<!-- daily-pr-task: playbook-change-scope-gate -->

Before applying a bootstrap change, operators should be able to review the intended host scope and whether the run has destructive effects. This offline gate validates dry-run evidence: an explicit inventory name, non-empty bounded host count, requested tags, and an operator acknowledgement for destructive changes. It validates supplied run metadata without connecting to an inventory.

## Portfolio Value

Adds a pre-apply review boundary to Ansible operations so host impact and destructive intent are explicit before automation changes infrastructure.

## Validation

Run `python3 -m unittest discover -s tests` and confirm bounded tagged scopes pass while default inventory names, invalid host counts, missing tags, unacknowledged destructive changes, and invalid limits fail.

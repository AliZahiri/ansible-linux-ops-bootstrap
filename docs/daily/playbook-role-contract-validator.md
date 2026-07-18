# Add playbook role contract validator

<!-- daily-pr-task: playbook-role-contract-validator -->

Playbooks should reference only local roles with an explicit task entrypoint. A lightweight validator can detect a renamed role or a missing `tasks/main.yml` before an operator discovers it during deployment. The validator operates only on repository files and does not need inventory credentials or host access.

## Portfolio Value

Adds deterministic guardrails for local Ansible role wiring, complementing syntax checks with a targeted repository contract.

## Validation

Run `python3 -m unittest discover -s tests` and confirm the validator accepts all current role entrypoints while reporting a missing role.

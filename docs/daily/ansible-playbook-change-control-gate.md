# Add Ansible playbook change control gate

<!-- daily-pr-task: ansible-playbook-change-control-gate -->

Operationally risky Ansible tasks should be reviewable before execution. This offline contract requires named tasks with explicit tags and requires command, shell, or reboot operations to carry a change ticket and rollback plan. It validates declared task metadata only and does not execute Ansible.

## Portfolio Value

Adds a deterministic review gate for operationally risky playbook actions without requiring inventory access or execution credentials.

## Validation

Run `python3 -m unittest discover -s tests` and confirm risky modules require explicit tags, a change ticket, and a rollback plan.

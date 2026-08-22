# Add Ansible role input contract gate

<!-- daily-pr-task: ansible-role-input-contract-gate -->

Validate that role defaults declare non-empty values for required operational inputs before a playbook is applied to a host inventory.

## Portfolio Value

Moves role configuration failures earlier, before host execution, while remaining inventory- and credential-free.

## Validation

Run `python3 -m unittest discover -s tests` and confirm blank or absent required role inputs fail deterministically.

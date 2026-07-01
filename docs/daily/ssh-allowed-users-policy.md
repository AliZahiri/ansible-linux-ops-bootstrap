# Add SSH allowed users policy

<!-- daily-pr-task: ssh-allowed-users-policy -->

SSH allowed users policy should keep interactive access explicit and auditable. Host bootstrap should restrict root login and render the allowed operator list from inventory.

Policy fields:

- allowed SSH users
- root login disabled
- password auth setting
- owner group

## Portfolio Value

Shows Linux hardening can restrict SSH entry points with an explicit allowlist.

## Validation

Run the unit test and confirm the sshd snippet uses templated allowed users and disables root login.

# Add sudoers admin group policy

<!-- daily-pr-task: sudoers-admin-group-policy -->

sudoers admin group policy should keep privilege escalation explicit, auditable, and validated before rollout.

Policy fields:

- admin group name
- password requirement
- visudo validation
- no user-specific broad grants

## Portfolio Value

Shows Linux bootstrap keeps privilege escalation explicit and group based.

## Validation

Run the unit test and confirm sudoers template uses an admin group and validates syntax.

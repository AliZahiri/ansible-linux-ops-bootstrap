# Add auditd baseline policy

<!-- daily-pr-task: auditd-baseline-policy -->

Audit baseline policy should watch sensitive authentication and privilege paths. This improves host investigation readiness after operational changes.

Watched paths:

- sshd configuration
- sudoers configuration
- user and group databases
- package manager history

## Portfolio Value

Shows Linux bootstrap includes audit visibility for sensitive system paths.

## Validation

Run the unit test and confirm audit rules watch SSH and sudoers paths.

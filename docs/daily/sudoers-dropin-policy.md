# Add sudoers drop-in policy

<!-- daily-pr-task: sudoers-dropin-policy -->

Deployment users should receive narrow sudo permissions instead of broad root access. A sudoers drop-in can document the exact operational commands allowed for automation.

Policy checks:

- deploy user variable is explicit
- allowed commands are narrow
- no blanket `ALL` command grant
- file mode is managed by Ansible

## Portfolio Value

Shows safer privilege boundaries for deployment users on Linux hosts.

## Validation

Run the unit test and confirm sudoers drop-in does not grant broad ALL privileges.

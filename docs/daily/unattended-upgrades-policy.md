# Add unattended upgrades policy

<!-- daily-pr-task: unattended-upgrades-policy -->

Unattended upgrades should be configured intentionally so security patches are applied while reboot behavior remains controlled.

Policy fields:

- security origin
- automatic reboot setting
- reboot time
- package blacklist hook

## Portfolio Value

Shows host bootstrap includes patching behavior with controlled reboot policy.

## Validation

Run the unit test and confirm security updates and reboot policy are explicit.

# Add sysctl hardening policy

<!-- daily-pr-task: sysctl-hardening-policy -->

Sysctl hardening should define baseline kernel networking protections for Linux hosts. Settings should be templated and reviewed before production rollout.

Baseline settings:

- disable IP forwarding by default
- disable source routing
- enable reverse path filtering
- ignore ICMP redirects

## Portfolio Value

Shows host bootstrap includes kernel networking hardening.

## Validation

Run the unit test and confirm key sysctl settings are templated.

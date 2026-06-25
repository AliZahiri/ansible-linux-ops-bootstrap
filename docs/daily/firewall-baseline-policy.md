# Add firewall baseline policy

<!-- daily-pr-task: firewall-baseline-policy -->

A firewall baseline should make inbound access explicit. SSH should be limited to trusted networks, and application ports should be declared by variable rather than hidden in role logic.

Baseline rules:

- default deny inbound
- allow trusted SSH networks
- allow declared application ports
- keep rule comments reviewable

## Portfolio Value

Shows host hardening includes explicit inbound access rules, not only package installation.

## Validation

Run the unit test and confirm SSH and application ports are explicit.

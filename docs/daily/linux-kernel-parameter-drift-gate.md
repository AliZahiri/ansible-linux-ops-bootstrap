# Add Linux kernel parameter drift gate

<!-- daily-pr-task: linux-kernel-parameter-drift-gate -->

Kernel hardening should be verified against observed runtime values after automation. This offline gate validates named unique parameters, compares expected and observed values, requires a timezone-aware observation, and reports whether a reboot still blocks convergence.

## Portfolio Value

Closes the gap between rendered sysctl policy and runtime kernel state with deterministic drift and reboot-readiness evidence.

## Validation

Run python3 -m unittest discover -s tests and confirm duplicate, drifted, malformed, reboot-pending, or naive-timestamped evidence fails.

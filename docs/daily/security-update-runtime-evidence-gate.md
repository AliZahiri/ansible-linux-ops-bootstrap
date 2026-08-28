# Add security update runtime evidence gate

<!-- daily-pr-task: security-update-runtime-evidence-gate -->

Rendering an unattended-upgrades policy does not prove that hosts are current. This offline gate validates supplied per-host runtime evidence: unique host identities, fresh timezone-aware observations, bounded pending and failed security updates, and explicit reboot state. It consumes exported counts only and does not require production inventory or package-manager access in CI.

## Portfolio Value

Connects unattended-upgrades intent to fresh, deterministic host evidence so pending or failed security updates and reboot debt are visible before compliance is claimed.

## Validation

Run python3 -m unittest discover -s tests and confirm stale, future-dated, duplicate, malformed, over-budget, failed, or reboot-pending host evidence fails.

# Add firewall ruleset drift evidence gate

<!-- daily-pr-task: firewall-ruleset-drift-evidence-gate -->

A correct Ansible firewall template does not prove that the live host still enforces it. This offline gate compares expected and observed service allowlists, requires a default-deny input policy, validates a fresh timezone-aware observation, and avoids storing production addresses or packet data.

## Portfolio Value

Adds live-state drift evidence to the firewall role story, detecting both accidental exposure and missing required access without committing real host inventories.

## Validation

Run python3 -m unittest discover -s tests and confirm a fresh exact default-deny ruleset passes while open defaults, missing or unexpected services, stale or future observations, absent digest, malformed evidence, and invalid policy fail.

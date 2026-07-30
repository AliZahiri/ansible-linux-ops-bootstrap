# Add firewall lockout safety gate

<!-- daily-pr-task: firewall-lockout-safety-gate -->

Applying a valid firewall ruleset can still lock operators out if the management source is absent or no timed rollback is armed. This dependency-free preflight validates the management CIDR and SSH port, requires an established management session and successful policy validation, and confirms a timezone-aware rollback deadline within a bounded emergency window. It validates evidence only and never reads inventory or changes a host.

## Portfolio Value

Adds an auditable safety gate that prevents firewall rollout without a proven management path and bounded automatic rollback, while remaining inventory- and credential-free.

## Validation

Run `python3 -m unittest discover -s tests` and confirm validated management access with timed rollback passes while invalid CIDR/port, missing session or policy evidence, absent rollback identity, stale/naive/excessive deadlines, and invalid policy values fail.

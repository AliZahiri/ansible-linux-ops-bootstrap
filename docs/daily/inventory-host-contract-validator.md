# Add inventory host contract validator

<!-- daily-pr-task: inventory-host-contract-validator -->

Inventory should be validated before Ansible connects to any host. This lightweight INI contract requires hosts to appear under named groups, rejects duplicate aliases, and blocks inline password, private-key, or vault-password variables. It operates on repository text only and complements Ansible syntax checks without requiring production inventory.

## Portfolio Value

Adds a credential-safe inventory preflight that catches structural mistakes and secret-bearing host variables before Ansible reaches a server.

## Validation

Run `python3 -m unittest discover -s tests` and confirm valid grouped hosts pass while duplicates, empty inventory, and inline sensitive variables fail.

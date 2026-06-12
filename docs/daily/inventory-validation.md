# Add inventory validation notes

<!-- daily-pr-task: inventory-validation -->

Inventory validation should happen before running playbooks against production hosts. A small mistake in group membership or host variables can apply roles to the wrong server.

Validation checks:

- expected host groups exist
- hostnames and IPs are documented
- SSH user is explicit
- production and sample inventories are separate
- sensitive variables are not committed in plain text

## Portfolio Value

Shows operational caution around Ansible-driven server changes.

## Validation

Review the markdown file and confirm it separates sample and production inventory concerns.

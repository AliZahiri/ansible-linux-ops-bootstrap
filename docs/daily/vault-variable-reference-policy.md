# Add vault variable reference policy

<!-- daily-pr-task: vault-variable-reference-policy -->

Secret-looking Ansible variables should resolve through vault references rather than plaintext values in ordinary group variables. The helper evaluates already parsed mappings, requires a configurable vault prefix, and reports exact variable names without ever logging their values.

## Portfolio Value

Adds a deterministic Ansible Vault hygiene control that reports risky variable names without exposing or parsing secret values.

## Validation

Run `python3 -m unittest discover -s tests` and confirm vault references pass, plaintext secret variables are named but values are never returned, and invalid policy configuration fails.

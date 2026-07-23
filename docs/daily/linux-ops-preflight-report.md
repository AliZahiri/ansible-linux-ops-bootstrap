# Add Linux operations preflight report

<!-- daily-pr-task: linux-ops-preflight-report -->

Before an operator runs a playbook, repository-local inventory structure, vault references, and role entrypoints should be evaluated together. This preflight returns only violation identifiers and variable names; it never emits secret values or contacts managed hosts.

## Portfolio Value

Connects inventory, Vault, and role validation into a credential-safe operator preflight that runs before host access.

## Validation

Run `python3 -m unittest discover -s tests` and confirm valid repository contracts pass while failures are partitioned without returning secret values.

# Add Ansible Vault guidance

<!-- daily-pr-task: ansible-vault-guidance -->

Secrets should be kept out of inventories and role defaults. Ansible Vault can protect sensitive values while keeping automation repeatable.

Vault usage guidance:

- store secrets in encrypted variable files
- keep sample variables non-sensitive
- document required variable names
- avoid putting vault passwords in the repository
- test playbooks with a non-production vault first

Vault password handling:

- keep the real vault file at `group_vars/vault.yml`
- encrypt it with `ansible-vault encrypt group_vars/vault.yml`
- pass the password interactively with `--ask-vault-pass`, or point `ANSIBLE_VAULT_PASSWORD_FILE` at a local file outside Git
- do not commit `.vault-pass`, CI secrets exports, or decrypted vault files

## Portfolio Value

Improves the security story for Ansible-based operational automation.

## Validation

Review the markdown file and confirm it does not include real secret examples.

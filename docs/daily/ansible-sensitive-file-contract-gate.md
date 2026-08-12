# Add Ansible sensitive-file contract gate

<!-- daily-pr-task: ansible-sensitive-file-contract-gate -->

Managed SSH, sudoers, and private-certificate files need an explicit ownership and permission contract. This offline gate validates supplied Ansible result metadata: unique approved paths, root ownership, a restrictive allowlisted mode, an immutable SHA-256 observation, and the role that managed the file. It does not read host files or execute a playbook.

## Portfolio Value

Extends the repository's hardening evidence beyond sudoers by making ownership, restrictive modes, hashes, and Ansible role attribution explicit for sensitive managed files.

## Validation

Run `python3 -m unittest discover -s tests` and confirm compliant sensitive-file evidence passes while empty input, unapproved and duplicate paths, non-root ownership, weak modes, invalid hashes, missing role attribution, and invalid root policies fail.

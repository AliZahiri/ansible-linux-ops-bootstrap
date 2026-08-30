# Add sudo command scope contract gate

<!-- daily-pr-task: sudo-command-scope-contract-gate -->

A valid sudoers file can still grant excessive privilege through `ALL`, shells, interpreters, wildcards, or indefinite passwordless access. This offline gate validates declarative grant metadata before template rendering: unique grant IDs, named subjects and run-as users, absolute literal command paths, forbidden shell and environment launchers, and ticketed time-bounded NOPASSWD exceptions.

## Portfolio Value

Moves sudo hardening from syntax-only validation to explicit least-privilege command scope and auditable temporary NOPASSWD exceptions, without committing real users, inventories, or sudoers credentials.

## Validation

Run python3 -m unittest discover -s tests and confirm literal command grants pass while ALL, shells, interpreters, wildcards, malformed commands, duplicate grants, unapproved or unbounded NOPASSWD access, and invalid policy fail.

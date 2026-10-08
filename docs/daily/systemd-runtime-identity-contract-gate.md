# Add systemd runtime identity contract gate

<!-- daily-pr-task: systemd-runtime-identity-contract-gate -->

Service isolation also requires an intentional runtime identity. This offline contract rejects root execution, requires a named user and group, and makes supplementary privilege groups explicit before a unit definition is promoted.

## Portfolio Value

Extends systemd hardening with a clear least-privilege runtime identity contract for platform services.

## Validation

Run python3 -m unittest discover -s tests and confirm non-root user/group identities and unique optional groups pass.

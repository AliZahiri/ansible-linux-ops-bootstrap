# Add temporary privileged account expiry gate

<!-- daily-pr-task: temporary-privileged-account-expiry-gate -->

Temporary privileged Linux access should be attributable and expire within a bounded window. This offline gate validates supplied account metadata: unique usernames, approved ticket and reviewer evidence, locked passwords, at least one SSH key, and timezone-aware expirations that are active but do not exceed policy.

## Portfolio Value

Adds auditable least-privilege controls for time-bound Linux administration without storing SSH keys, account databases, or production inventories in the repository.

## Validation

Run python3 -m unittest discover -s tests and confirm missing approvals, duplicate users, unlocked passwords, absent keys, invalid or expired timestamps, excessive validity, malformed records, and invalid policy fail.

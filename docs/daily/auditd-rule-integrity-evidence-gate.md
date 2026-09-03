# Add auditd rule integrity evidence gate

<!-- daily-pr-task: auditd-rule-integrity-evidence-gate -->

A baseline template does not prove that the loaded auditd rule set is active, complete, or recently observed. This offline evidence gate validates service state, loaded-rule count, a SHA-256 ruleset digest, and a bounded observation time. Rule immutability is an explicit optional policy because enabling it has operational consequences during change windows.

## Portfolio Value

Turns static auditd baseline intent into fresh, reviewable effective-state evidence while keeping immutable-rule enforcement an explicit operational choice.

## Validation

Run python3 -m unittest discover -s tests and confirm fresh active loaded rule evidence with a valid digest passes while inactive, stale, malformed, and policy-invalid evidence fails.

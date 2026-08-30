# Add mandatory access control evidence gate

<!-- daily-pr-task: mandatory-access-control-evidence-gate -->

Linux hardening should verify that a mandatory access control framework is actively enforcing policy, not merely installed. This offline gate validates per-host SELinux or AppArmor evidence: unique host identity, enforcing mode, a named loaded policy, positive enforced-profile coverage, reviewed denial events, and a fresh timezone-aware observation.

## Portfolio Value

Adds portable SELinux/AppArmor verification evidence to the Linux baseline and distinguishes configured packages from actively enforced, recently reviewed host policy without requiring production inventory in CI.

## Validation

Run python3 -m unittest discover -s tests and confirm fresh SELinux/AppArmor enforcement evidence passes while duplicate hosts, permissive or unknown frameworks, missing profiles, unreviewed denials, stale observations, and invalid policy fail.

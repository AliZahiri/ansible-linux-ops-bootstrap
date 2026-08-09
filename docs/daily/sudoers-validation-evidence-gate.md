# Add sudoers validation evidence gate

<!-- daily-pr-task: sudoers-validation-evidence-gate -->

A malformed or over-permissive sudoers fragment can lock operators out or grant unintended privilege during bootstrap. This offline gate validates supplied deployment evidence: unique files under /etc/sudoers.d, root ownership, mode 0440, a valid SHA-256 digest, successful visudo syntax validation, and a fresh timezone-aware verification timestamp. It never reads production sudoers content.

## Portfolio Value

Adds reviewable evidence for the highest-risk privilege-escalation files so Ansible hardening cannot report success without secure ownership, permissions, integrity, and syntax checks.

## Validation

Run `python3 -m unittest discover -s tests` and confirm secure fresh visudo evidence passes while empty input, unsafe paths, duplicate fragments, wrong ownership or mode, malformed digests, failed checks, stale or naive timestamps, and invalid policies fail.

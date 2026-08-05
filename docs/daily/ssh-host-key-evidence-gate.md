# Add SSH host key evidence gate

<!-- daily-pr-task: ssh-host-key-evidence-gate -->

Ansible SSH hardening is incomplete if the controller can silently accept an unverified replacement host key. This offline gate validates unique inventory hosts, strict host-key checking, OpenSSH SHA-256 fingerprints, and fresh timezone-aware verification evidence. It consumes supplied evidence only and never opens an SSH connection or reads private keys.

## Portfolio Value

Extends SSH hardening to the Ansible control-plane trust boundary, preventing stale or permissive host-key verification evidence from silently weakening automation.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unique strict fresh evidence passes while empty input, duplicate hosts, disabled checking, malformed fingerprints, stale or naive timestamps, and invalid age policy values fail.

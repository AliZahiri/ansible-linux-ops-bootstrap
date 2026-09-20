# Changelog

All notable changes to this project are documented in this file.

The project follows Semantic Versioning for public release snapshots. The
validation helpers inspect supplied configuration and evidence; they do not
replace an operator's change review or a live restore drill.

## [0.2.0] - Unreleased

### Added

- Evidence validators for backup freshness, encryption, manifests, recovery
  points, restore execution, checksums, immutability, and retention.
- Linux operations controls for audit logging, file-integrity monitoring,
  firewall drift, DNS health, package-manager locks, kernel settings, systemd
  restart/resource limits, and temporary privileged accounts.
- SSH and privilege-boundary contracts covering authentication methods,
  cryptographic algorithms, host-key evidence, lockout-safe hardening, sudo
  command scope, and mandatory access control.
- Ansible inventory, role, collection, handler-notification, and playbook
  change-control validation helpers.
- Offline evidence examples and unit coverage for the new operational gates.

### Changed

- SSH hardening remains opt-in and now fails closed unless the allowed-user
  contract and a non-empty authorized-keys file are present.
- CI validates Python behavior and Ansible syntax against the sample inventory.
- Daily portfolio automation validates generated destinations and performs
  checks in an isolated worktree before a pull request can merge.

### Security

- The repository contains only sample inventory values and placeholder vault
  references; production credentials, private keys, and vault passwords remain
  outside Git.
- Validation controls bind supplied evidence to the reviewed inventory and
  playbook rather than treating an unbound report as proof of execution.

### Compatibility

- Existing `bootstrap.yml`, `monitoring.yml`, and `backup.yml` playbooks remain
  the supported entry points.
- No production inventory, secret migration, or live-host change is performed
  by this release.

[0.2.0]: https://github.com/AliZahiri/ansible-linux-ops-bootstrap/compare/v0.1.0...v0.2.0

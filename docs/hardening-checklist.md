# Linux Operations Hardening Checklist

## Access

- Disable password-based SSH login where possible.
- Use named users and sudo instead of direct root login.
- Keep SSH keys rotated and documented.
- Restrict SSH access by network when possible.

## Packages

- Enable unattended security updates when appropriate.
- Remove unused packages and services.
- Keep Docker and Compose versions documented.

## Firewall

- Default deny incoming traffic.
- Allow only required service ports.
- Keep monitoring ports private unless explicitly required.

## Observability

- Install Node Exporter on every host.
- Track CPU, memory, disk, network, and systemd service health.
- Alert on disk pressure, load, and service failures.

## Backups

- Backup application data, databases, and configuration.
- Test restore procedures regularly.
- Keep backup credentials outside repositories.

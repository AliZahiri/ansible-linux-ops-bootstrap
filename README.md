# Ansible Linux Ops Bootstrap

Production-oriented Ansible baseline for preparing Linux servers for Docker Compose workloads, monitoring, and operational automation.

This repository is designed as a practical bootstrap kit for small and medium production environments where teams need repeatable server setup without introducing a full platform stack on day one.

## What This Covers

- Base Linux packages and timezone setup
- Operations user and SSH hardening baseline
- UFW firewall rules
- Docker installation and service enablement
- Node Exporter installation for Prometheus monitoring
- Backup script template for PostgreSQL-style workloads
- Hardening and operations checklist

## Structure

```text
.
├── ansible.cfg
├── group_vars/
│   └── all.yml
├── inventories/
│   └── sample/
│       └── hosts.ini
├── playbooks/
│   ├── backup.yml
│   ├── bootstrap.yml
│   └── monitoring.yml
└── roles/
    ├── backup/
    ├── common/
    ├── docker/
    ├── firewall/
    └── node_exporter/
```

## Quick Start

```bash
cp inventories/sample/hosts.ini inventories/production.ini
ansible-playbook -i inventories/production.ini playbooks/bootstrap.yml
ansible-playbook -i inventories/production.ini playbooks/monitoring.yml
ansible-playbook -i inventories/production.ini playbooks/backup.yml
```

## Inventory Example

```ini
[app]
app-01 ansible_host=10.10.10.11

[monitoring]
monitoring-01 ansible_host=10.10.10.20
```

## Production Notes

- Use Ansible Vault for secrets.
- Review firewall ports before running against production servers.
- Prefer a non-root SSH user with sudo access.
- Keep backup credentials outside Git.
- Test restore paths, not only backup creation.
- Pin exporter versions and review checksums for stricter environments.

## Next Iterations

- Add Docker Compose app deployment role
- Add PostgreSQL backup and restore role
- Add Loki/Promtail role
- Add SSH policy templates
- Add CIS-inspired hardening tasks

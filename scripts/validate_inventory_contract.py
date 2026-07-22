from __future__ import annotations

import re


_SENSITIVE = re.compile(r"(?:ansible_password|ansible_ssh_pass|ansible_private_key_file|vault_password_file)\s*=", re.IGNORECASE)


def inventory_contract_violations(content: str) -> tuple[str, ...]:
    violations: list[str] = []
    group = ""
    seen_hosts: set[str] = set()
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            group = line[1:-1].strip()
            if not group:
                violations.append(f"line_{line_number}:inventory_group_name_is_required")
            continue
        if _SENSITIVE.search(line):
            violations.append(f"line_{line_number}:inline_sensitive_inventory_variable_is_forbidden")
        if not group or group.endswith((":vars", ":children")):
            continue
        host = line.split()[0]
        if host in seen_hosts:
            violations.append(f"line_{line_number}:duplicate_host_alias:{host}")
        seen_hosts.add(host)
    if not seen_hosts:
        violations.append("inventory_requires_at_least_one_grouped_host")
    return tuple(violations)


def inventory_contract_is_valid(content: str) -> bool:
    return not inventory_contract_violations(content)

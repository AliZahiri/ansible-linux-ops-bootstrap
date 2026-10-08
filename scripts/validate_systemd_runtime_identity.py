from __future__ import annotations


def systemd_runtime_identity_violations(settings: object) -> tuple[str, ...]:
    if not isinstance(settings, dict): return ("runtime_identity_must_be_an_object",)
    violations: list[str] = []
    for field in ("User", "Group"):
        value = settings.get(field)
        if not isinstance(value, str) or not value.strip() or value == "root": violations.append(f"{field}_must_be_a_non_root_identity")
    groups = settings.get("SupplementaryGroups", [])
    if not isinstance(groups, list) or any(not isinstance(group, str) or not group.strip() for group in groups) or len(set(groups)) != len(groups): violations.append("SupplementaryGroups_must_be_unique_non_empty_strings")
    return tuple(violations)

def systemd_runtime_identity_is_safe(settings: object) -> bool: return not systemd_runtime_identity_violations(settings)

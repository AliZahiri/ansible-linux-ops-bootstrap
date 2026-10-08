from __future__ import annotations


_FORBIDDEN = frozenset({"CAP_SYS_ADMIN", "CAP_SYS_MODULE", "CAP_SYS_RAWIO"})


def systemd_capability_bounding_violations(settings: object) -> tuple[str, ...]:
    if not isinstance(settings, dict):
        return ("capability_settings_must_be_an_object",)
    violations: list[str] = []
    bounded = settings.get("CapabilityBoundingSet")
    if not isinstance(bounded, list) or not bounded or any(not isinstance(value, str) or not value.strip() for value in bounded):
        violations.append("CapabilityBoundingSet_must_be_a_non_empty_string_list")
    elif len(set(bounded)) != len(bounded) or _FORBIDDEN.intersection(bounded):
        violations.append("CapabilityBoundingSet_contains_duplicate_or_forbidden_capability")
    ambient = settings.get("AmbientCapabilities", [])
    if ambient not in ([], None):
        violations.append("AmbientCapabilities_must_be_empty")
    if settings.get("NoNewPrivileges") is not True:
        violations.append("NoNewPrivileges_must_be_enabled")
    return tuple(violations)


def systemd_capability_bounding_is_safe(settings: object) -> bool:
    return not systemd_capability_bounding_violations(settings)

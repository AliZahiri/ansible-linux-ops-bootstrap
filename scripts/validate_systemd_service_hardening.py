from __future__ import annotations


def systemd_service_hardening_violations(settings: object, *, required_read_write_paths: frozenset[str] = frozenset()) -> tuple[str, ...]:
    if not isinstance(required_read_write_paths, frozenset) or any(not isinstance(path, str) or not path.startswith("/") for path in required_read_write_paths):
        raise ValueError("required_read_write_paths must be a frozenset of absolute paths")
    if not isinstance(settings, dict):
        return ("systemd_hardening_settings_must_be_an_object",)
    violations: list[str] = []
    for key in ("NoNewPrivileges", "PrivateTmp", "ProtectHome"):
        if settings.get(key) is not True:
            violations.append(f"{key}_must_be_enabled")
    if settings.get("ProtectSystem") not in {"full", "strict"}:
        violations.append("ProtectSystem_must_be_full_or_strict")
    writable = settings.get("ReadWritePaths", [])
    if not isinstance(writable, list) or any(not isinstance(path, str) or not path.startswith("/") for path in writable):
        violations.append("ReadWritePaths_must_be_a_list_of_absolute_paths")
    elif not required_read_write_paths.issubset(set(writable)):
        violations.append("ReadWritePaths_must_include_required_paths")
    return tuple(violations)


def systemd_service_is_hardened(settings: object, **policy: object) -> bool:
    return not systemd_service_hardening_violations(settings, **policy)

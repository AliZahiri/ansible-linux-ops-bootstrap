from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def package_manager_lock_violations(hosts: list[dict[str, object]], *, now: datetime, maximum_evidence_age_seconds: int = 300, maximum_owner_age_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    for name, value in (("maximum_evidence_age_seconds", maximum_evidence_age_seconds), ("maximum_owner_age_seconds", maximum_owner_age_seconds)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if not isinstance(hosts, list) or not hosts:
        return ("package_manager_lock_evidence_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for index, host in enumerate(hosts):
        if not isinstance(host, dict):
            violations.append(f"host_{index}:must_be_an_object")
            continue
        host_id = host.get("host_id")
        if not isinstance(host_id, str) or not host_id.strip():
            violations.append(f"host_{index}:host_id_is_required")
        elif host_id in seen:
            violations.append(f"host_{index}:host_id_must_be_unique")
        else:
            seen.add(host_id)
        observed_at = _timestamp(host.get("observed_at"))
        if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_evidence_age_seconds:
            violations.append(f"host_{index}:observation_is_stale_or_invalid")
        lock_held = host.get("lock_held")
        if not isinstance(lock_held, bool):
            violations.append(f"host_{index}:lock_held_must_be_boolean")
            continue
        if not lock_held:
            continue
        violations.append(f"host_{index}:package_manager_lock_is_held")
        owner_pid, owner_command = host.get("owner_pid"), host.get("owner_command")
        if not isinstance(owner_pid, int) or isinstance(owner_pid, bool) or owner_pid < 1:
            violations.append(f"host_{index}:lock_owner_pid_is_required")
        if not isinstance(owner_command, str) or not owner_command.strip():
            violations.append(f"host_{index}:lock_owner_command_is_required")
        owner_started_at = _timestamp(host.get("owner_started_at"))
        if owner_started_at is None:
            violations.append(f"host_{index}:lock_owner_started_at_is_required")
        elif not 0 <= (now - owner_started_at).total_seconds() <= maximum_owner_age_seconds:
            violations.append(f"host_{index}:lock_owner_exceeds_review_window")
    return tuple(violations)


def package_manager_is_ready(hosts: list[dict[str, object]], **policy: object) -> bool:
    return not package_manager_lock_violations(hosts, **policy)

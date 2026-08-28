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


def security_update_evidence_violations(hosts: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 86400, maximum_pending: int = 0, maximum_failed: int = 0) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    for name, value in (("maximum_age_seconds", maximum_age_seconds), ("maximum_pending", maximum_pending), ("maximum_failed", maximum_failed)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if not isinstance(hosts, list) or not hosts:
        return ("at_least_one_host_evidence_record_is_required",)
    violations: list[str] = []
    seen_hosts: set[str] = set()
    for index, host in enumerate(hosts):
        if not isinstance(host, dict):
            violations.append(f"host_{index}:must_be_an_object")
            continue
        host_id = host.get("host_id")
        if not isinstance(host_id, str) or not host_id.strip():
            violations.append(f"host_{index}:host_id_is_required")
        elif host_id in seen_hosts:
            violations.append(f"host_{index}:host_id_must_be_unique")
        else:
            seen_hosts.add(host_id)
        observed_at = _timestamp(host.get("observed_at"))
        if observed_at is None:
            violations.append(f"host_{index}:observed_at_must_be_timezone_aware")
        elif not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
            violations.append(f"host_{index}:evidence_is_stale_or_future_dated")
        for field, budget in (("pending_security_updates", maximum_pending), ("failed_security_updates", maximum_failed)):
            value = host.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                violations.append(f"host_{index}:{field}_must_be_non_negative")
            elif value > budget:
                violations.append(f"host_{index}:{field}_exceeds_budget")
        if not isinstance(host.get("reboot_required"), bool):
            violations.append(f"host_{index}:reboot_required_must_be_boolean")
        elif host["reboot_required"]:
            violations.append(f"host_{index}:security_update_reboot_is_pending")
    return tuple(violations)


def security_update_evidence_is_healthy(hosts: list[dict[str, object]], **policy: object) -> bool:
    return not security_update_evidence_violations(hosts, **policy)

from __future__ import annotations

from datetime import datetime
import re


_UNIT = re.compile(r"[A-Za-z0-9][A-Za-z0-9@_.-]*\.service\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def systemd_resource_limit_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 900, minimum_nofile: int = 1024) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum evidence age must be a positive integer")
    if not isinstance(minimum_nofile, int) or isinstance(minimum_nofile, bool) or minimum_nofile <= 0:
        raise ValueError("minimum nofile limit must be a positive integer")

    violations: list[str] = []
    unit = evidence.get("unit")
    if not isinstance(unit, str) or not _UNIT.fullmatch(unit):
        violations.append("systemd_unit_name_is_invalid")
    if evidence.get("active") is not True:
        violations.append("systemd_unit_must_be_active")
    if evidence.get("configuration_read") is not True:
        violations.append("systemd_configuration_must_be_read")
    for field in ("memory_max_bytes", "tasks_max"):
        value = evidence.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            violations.append(f"{field}_must_be_positive")
    nofile = evidence.get("limit_nofile")
    if not isinstance(nofile, int) or isinstance(nofile, bool) or nofile < minimum_nofile:
        violations.append("limit_nofile_is_below_minimum")

    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    else:
        age = (now - observed_at).total_seconds()
        if age < 0:
            violations.append("resource_limit_evidence_is_in_the_future")
        elif age > maximum_age_seconds:
            violations.append("resource_limit_evidence_is_stale")
    return tuple(violations)


def systemd_resource_limits_are_verified(evidence: dict[str, object], **policy: object) -> bool:
    return not systemd_resource_limit_evidence_violations(evidence, **policy)

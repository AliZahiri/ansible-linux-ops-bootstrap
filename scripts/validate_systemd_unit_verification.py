from __future__ import annotations

from datetime import datetime
import re


_UNIT = re.compile(r"[A-Za-z0-9_.@-]+\.(service|socket|timer|target)\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def systemd_unit_verification_violations(evidence: dict[str, object], *, now: datetime, maximum_restart_count: int = 0, maximum_observation_age_seconds: int = 300) -> tuple[str, ...]:
    if not isinstance(maximum_restart_count, int) or isinstance(maximum_restart_count, bool) or maximum_restart_count < 0:
        raise ValueError("maximum restart count must be a non-negative integer")
    if not isinstance(maximum_observation_age_seconds, int) or isinstance(maximum_observation_age_seconds, bool) or maximum_observation_age_seconds <= 0:
        raise ValueError("maximum observation age must be a positive integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    violations: list[str] = []
    unit = evidence.get("unit")
    if not isinstance(unit, str) or not _UNIT.fullmatch(unit):
        violations.append("systemd_unit_name_is_invalid")
    if evidence.get("daemon_reload_completed") is not True:
        violations.append("daemon_reload_must_be_confirmed")
    if evidence.get("enabled") is not True:
        violations.append("systemd_unit_must_be_enabled")
    if evidence.get("active") is not True:
        violations.append("systemd_unit_must_be_active")
    if evidence.get("result") != "success":
        violations.append("systemd_unit_result_must_be_success")
    restart_count = evidence.get("restart_count")
    if not isinstance(restart_count, int) or isinstance(restart_count, bool) or restart_count < 0:
        violations.append("restart_count_must_be_a_non_negative_integer")
    elif restart_count > maximum_restart_count:
        violations.append("restart_count_exceeds_maximum")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    else:
        age = (now - observed_at).total_seconds()
        if age < 0:
            violations.append("systemd_observation_is_in_the_future")
        elif age > maximum_observation_age_seconds:
            violations.append("systemd_observation_is_stale")
    return tuple(violations)


def systemd_unit_is_verified(evidence: dict[str, object], **policy: object) -> bool:
    return not systemd_unit_verification_violations(evidence, **policy)

from __future__ import annotations

from datetime import datetime


def backup_key_rotation_violations(evidence: dict[str, object], *, now: datetime, maximum_age_days: int = 90) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_days, int) or isinstance(maximum_age_days, bool) or maximum_age_days <= 0:
        raise ValueError("maximum key age must be positive")
    violations: list[str] = []
    if evidence.get("key_id") in (None, ""):
        violations.append("key_id_is_required")
    if evidence.get("active") is not True:
        violations.append("backup_key_must_be_active")
    value = evidence.get("rotated_at")
    try:
        rotated_at = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
    except ValueError:
        rotated_at = None
    if rotated_at is None or rotated_at.tzinfo is None or rotated_at.utcoffset() is None:
        violations.append("rotated_at_must_be_timezone_aware")
    elif not 0 <= (now - rotated_at).days <= maximum_age_days:
        violations.append("backup_key_rotation_is_stale")
    return tuple(violations)


def backup_key_rotation_is_current(evidence: dict[str, object], **policy: object) -> bool:
    return not backup_key_rotation_violations(evidence, **policy)

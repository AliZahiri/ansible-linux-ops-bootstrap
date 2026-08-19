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


def backup_key_rotation_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_days: int = 90) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_days, int) or isinstance(maximum_age_days, bool) or maximum_age_days <= 0:
        raise ValueError("maximum key age must be positive")
    violations: list[str] = []
    for field in ("key_id", "backup_scope"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    if evidence.get("active") is not True:
        violations.append("backup_key_must_be_active")
    if evidence.get("rotation_verified") is not True:
        violations.append("rotation_verification_must_pass")
    rotated_at, expires_at = _timestamp(evidence.get("rotated_at")), _timestamp(evidence.get("expires_at"))
    if rotated_at is None:
        violations.append("rotated_at_must_be_timezone_aware")
    elif not 0 <= (now - rotated_at).days <= maximum_age_days:
        violations.append("key_rotation_is_not_fresh")
    if expires_at is None:
        violations.append("expires_at_must_be_timezone_aware")
    elif expires_at <= now:
        violations.append("backup_key_must_not_be_expired")
    elif rotated_at is not None and expires_at <= rotated_at:
        violations.append("key_expiry_must_follow_rotation")
    return tuple(violations)


def backup_key_rotation_evidence_is_valid(evidence: dict[str, object], **policy: object) -> bool:
    return not backup_key_rotation_evidence_violations(evidence, **policy)

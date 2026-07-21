from __future__ import annotations

from datetime import datetime


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def restore_rto_violations(evidence: dict[str, object], *, max_duration_seconds: int) -> tuple[str, ...]:
    if not isinstance(max_duration_seconds, int) or isinstance(max_duration_seconds, bool) or max_duration_seconds <= 0:
        raise ValueError("maximum duration must be a positive integer")
    violations: list[str] = []
    if evidence.get("checksum_verified") is not True:
        violations.append("backup_checksum_not_verified")
    if evidence.get("application_verification_passed") is not True:
        violations.append("application_verification_not_passed")
    started = _parse_timestamp(evidence.get("started_at"))
    completed = _parse_timestamp(evidence.get("completed_at"))
    if started is None or completed is None:
        violations.append("timezone_aware_restore_window_is_required")
    elif completed < started:
        violations.append("restore_window_is_reversed")
    elif (completed - started).total_seconds() > max_duration_seconds:
        violations.append("restore_exceeds_recovery_time_objective")
    return tuple(violations)


def restore_meets_rto(evidence: dict[str, object], *, max_duration_seconds: int) -> bool:
    return not restore_rto_violations(evidence, max_duration_seconds=max_duration_seconds)

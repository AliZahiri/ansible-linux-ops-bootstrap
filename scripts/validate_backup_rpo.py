from __future__ import annotations

from datetime import datetime


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    return parsed


def backup_rpo_violations(*, last_success_at: str, observed_at: str, max_age_seconds: int) -> tuple[str, ...]:
    if not isinstance(max_age_seconds, int) or isinstance(max_age_seconds, bool) or max_age_seconds <= 0:
        raise ValueError("maximum age must be a positive integer")
    last_success = _parse_timestamp(last_success_at)
    observed = _parse_timestamp(observed_at)
    age_seconds = (observed - last_success).total_seconds()
    if age_seconds < 0:
        return ("backup_timestamp_is_in_the_future",)
    if age_seconds > max_age_seconds:
        return ("backup_exceeds_recovery_point_objective",)
    return ()


def backup_meets_rpo(*, last_success_at: str, observed_at: str, max_age_seconds: int) -> bool:
    return not backup_rpo_violations(last_success_at=last_success_at, observed_at=observed_at, max_age_seconds=max_age_seconds)

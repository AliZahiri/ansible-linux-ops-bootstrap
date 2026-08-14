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


def docker_daemon_runtime_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 900) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum evidence age must be positive")
    violations: list[str] = []
    if evidence.get("live_restore") is not True:
        violations.append("live_restore_must_be_enabled")
    if evidence.get("rootless") is not True and evidence.get("userns_remap") is not True:
        violations.append("rootless_or_userns_remap_is_required")
    if evidence.get("log_driver") not in {"json-file", "local", "journald"}:
        violations.append("log_driver_must_be_supported")
    max_size, max_file = evidence.get("log_max_size_mb"), evidence.get("log_max_files")
    if not isinstance(max_size, int) or isinstance(max_size, bool) or not 1 <= max_size <= 100:
        violations.append("log_max_size_mb_must_be_between_1_and_100")
    if not isinstance(max_file, int) or isinstance(max_file, bool) or not 2 <= max_file <= 20:
        violations.append("log_max_files_must_be_between_2_and_20")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    elif not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
        violations.append("daemon_evidence_is_not_fresh")
    return tuple(violations)


def docker_daemon_runtime_is_safe(evidence: dict[str, object], **policy: object) -> bool:
    return not docker_daemon_runtime_violations(evidence, **policy)

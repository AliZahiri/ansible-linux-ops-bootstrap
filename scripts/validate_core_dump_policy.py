from __future__ import annotations

from datetime import datetime


def core_dump_policy_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be a positive integer")
    violations: list[str] = []
    if evidence.get("systemd_coredump_storage") != "none":
        violations.append("systemd_coredump_storage_must_be_none")
    if evidence.get("process_core_limit_bytes") != 0:
        violations.append("process_core_limit_must_be_zero")
    if evidence.get("fs_suid_dumpable") != 0:
        violations.append("suid_dumping_must_be_disabled")
    pattern = evidence.get("kernel_core_pattern")
    if not isinstance(pattern, str) or pattern.strip() not in {"|/bin/false", "/dev/null"}:
        violations.append("kernel_core_pattern_must_discard_dumps")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    elif not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
        violations.append("core_dump_policy_evidence_is_stale_or_future_dated")
    return tuple(violations)


def core_dump_policy_is_hardened(evidence: dict[str, object], **policy: object) -> bool:
    return not core_dump_policy_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"(?:sha256:)?[0-9a-f]{64}\Z")


def file_integrity_monitor_violations(evidence: dict[str, object], *, now: datetime, maximum_scan_age_seconds: int = 86400, maximum_reviewed_changes: int = 0) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_scan_age_seconds, int) or isinstance(maximum_scan_age_seconds, bool) or maximum_scan_age_seconds < 1:
        raise ValueError("maximum_scan_age_seconds must be positive")
    if not isinstance(maximum_reviewed_changes, int) or isinstance(maximum_reviewed_changes, bool) or maximum_reviewed_changes < 0:
        raise ValueError("maximum_reviewed_changes must be non-negative")
    if not isinstance(evidence, dict):
        return ("file_integrity_evidence_must_be_an_object",)

    violations: list[str] = []
    if evidence.get("scheduler_active") is not True:
        violations.append("file_integrity_scheduler_must_be_active")
    digest = evidence.get("baseline_sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("file_integrity_baseline_sha256_must_be_a_digest")
    if evidence.get("scan_succeeded") is not True:
        violations.append("latest_file_integrity_scan_must_succeed")
    changed = evidence.get("reviewed_critical_change_count")
    if not isinstance(changed, int) or isinstance(changed, bool) or changed < 0:
        violations.append("reviewed_critical_change_count_must_be_non_negative")
    elif changed > maximum_reviewed_changes:
        violations.append("critical_file_changes_exceed_reviewed_budget")
    observed_at = _timestamp(evidence.get("scan_completed_at"))
    if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_scan_age_seconds:
        violations.append("file_integrity_scan_is_invalid_stale_or_future_dated")
    return tuple(violations)


def file_integrity_monitor_is_verified(evidence: dict[str, object], **policy: object) -> bool:
    return not file_integrity_monitor_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

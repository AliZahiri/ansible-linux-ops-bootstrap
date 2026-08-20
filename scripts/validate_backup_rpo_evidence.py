from __future__ import annotations

from datetime import datetime


def backup_rpo_evidence_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    rpo_minutes = evidence.get("rpo_minutes")
    observed_age_minutes = evidence.get("observed_age_minutes")
    if not isinstance(rpo_minutes, int) or isinstance(rpo_minutes, bool) or rpo_minutes < 1:
        violations.append("rpo_minutes_must_be_positive")
    if not isinstance(observed_age_minutes, int) or isinstance(observed_age_minutes, bool) or observed_age_minutes < 0:
        violations.append("observed_age_minutes_must_be_non_negative")
    elif isinstance(rpo_minutes, int) and not isinstance(rpo_minutes, bool) and rpo_minutes > 0 and observed_age_minutes > rpo_minutes:
        violations.append("backup_age_exceeds_rpo")
    verified_at = _parse_timestamp(evidence.get("verified_at"))
    if verified_at is None:
        violations.append("verified_at_must_be_timezone_aware")
    if evidence.get("verification_passed") is not True:
        violations.append("verification_must_pass")
    return tuple(violations)


def backup_rpo_evidence_is_valid(evidence: dict[str, object]) -> bool:
    return not backup_rpo_evidence_violations(evidence)


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

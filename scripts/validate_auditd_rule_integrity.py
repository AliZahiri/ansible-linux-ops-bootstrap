from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"(?:sha256:)?[0-9a-f]{64}\Z")


def auditd_rule_integrity_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 900, require_immutable_rules: bool = False) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum evidence age must be a positive integer")
    if not isinstance(require_immutable_rules, bool):
        raise ValueError("require immutable rules must be boolean")

    violations: list[str] = []
    if evidence.get("service_active") is not True:
        violations.append("auditd_service_must_be_active")
    if evidence.get("rules_loaded") is not True:
        violations.append("auditd_rules_must_be_loaded")
    rule_count = evidence.get("loaded_rule_count")
    if not isinstance(rule_count, int) or isinstance(rule_count, bool) or rule_count < 1:
        violations.append("loaded_rule_count_must_be_positive")
    digest = evidence.get("rules_sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("rules_sha256_must_be_a_sha256_digest")
    immutable = evidence.get("rules_immutable")
    if not isinstance(immutable, bool):
        violations.append("rules_immutable_must_be_boolean")
    elif require_immutable_rules and immutable is not True:
        violations.append("auditd_rules_must_be_immutable")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    elif not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
        violations.append("auditd_rule_evidence_is_stale_or_future_dated")
    return tuple(violations)


def auditd_rule_integrity_is_verified(evidence: dict[str, object], **policy: object) -> bool:
    return not auditd_rule_integrity_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

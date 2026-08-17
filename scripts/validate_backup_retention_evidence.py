from __future__ import annotations

from datetime import datetime


_REQUIRED_TIERS = frozenset({"daily", "weekly", "monthly"})


def backup_retention_evidence_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    tiers = evidence.get("tiers")
    if not isinstance(tiers, dict) or _REQUIRED_TIERS.difference(tiers):
        return ("required_retention_tiers_are_missing",)
    for tier in sorted(_REQUIRED_TIERS):
        value = tiers[tier]
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
        except ValueError:
            timestamp = None
        if timestamp is None or timestamp.tzinfo is None or timestamp.utcoffset() is None:
            violations.append(f"{tier}_oldest_retained_at_must_be_timezone_aware")
    if evidence.get("retention_verified") is not True:
        violations.append("retention_verification_must_pass")
    return tuple(violations)


def backup_retention_evidence_is_valid(evidence: dict[str, object]) -> bool:
    return not backup_retention_evidence_violations(evidence)

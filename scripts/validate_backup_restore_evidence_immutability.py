from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def restore_evidence_immutability_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(evidence.get("artifact_sha256"), str) or not _SHA256.fullmatch(evidence["artifact_sha256"]):
        violations.append("artifact_sha256_is_invalid")
    if evidence.get("immutable_storage") is not True:
        violations.append("immutable_storage_is_required")
    value = evidence.get("verified_at")
    try:
        verified_at = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
    except ValueError:
        verified_at = None
    if verified_at is None or verified_at.tzinfo is None or verified_at.utcoffset() is None:
        violations.append("verified_at_must_be_timezone_aware")
    if evidence.get("integrity_check_passed") is not True:
        violations.append("integrity_check_must_pass")
    if evidence.get("application_check_passed") is not True:
        violations.append("application_check_must_pass")
    return tuple(violations)


def restore_evidence_is_immutable(evidence: dict[str, object]) -> bool:
    return not restore_evidence_immutability_violations(evidence)

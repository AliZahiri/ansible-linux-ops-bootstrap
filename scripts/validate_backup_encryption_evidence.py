from __future__ import annotations

from datetime import datetime
import re


_KEY_REFERENCE = re.compile(r"(vault|kms|keyring)://[A-Za-z0-9][A-Za-z0-9._/:@-]{2,255}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def backup_encryption_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 3600, allowed_algorithms: tuple[str, ...] = ("AES-256-GCM", "CHACHA20-POLY1305")) -> tuple[str, ...]:
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum evidence age must be a positive integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not allowed_algorithms or any(not str(item).strip() for item in allowed_algorithms):
        raise ValueError("allowed algorithms must be non-empty")
    violations: list[str] = []
    if evidence.get("encrypted") is not True:
        violations.append("backup_must_be_encrypted")
    if evidence.get("algorithm") not in allowed_algorithms:
        violations.append("backup_encryption_algorithm_is_not_approved")
    key_reference = evidence.get("key_reference")
    if not isinstance(key_reference, str) or not _KEY_REFERENCE.fullmatch(key_reference):
        violations.append("external_key_reference_is_invalid")
    if evidence.get("checksum_verified") is not True:
        violations.append("encrypted_backup_checksum_must_be_verified")
    if evidence.get("plaintext_removed") is not True:
        violations.append("plaintext_backup_material_must_be_removed")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None:
        violations.append("observed_at_must_be_timezone_aware")
    else:
        age = (now - observed_at).total_seconds()
        if age < 0:
            violations.append("encryption_evidence_is_in_the_future")
        elif age > maximum_age_seconds:
            violations.append("encryption_evidence_is_stale")
    return tuple(violations)


def backup_encryption_evidence_is_acceptable(evidence: dict[str, object], **policy: object) -> bool:
    return not backup_encryption_evidence_violations(evidence, **policy)

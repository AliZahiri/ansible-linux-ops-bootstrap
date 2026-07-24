from __future__ import annotations

from scripts.validate_backup_rpo import backup_rpo_violations
from scripts.validate_restore_rto import restore_rto_violations


def recovery_evidence_violations(*, evidence: dict[str, object], observed_at: str, max_age_seconds: int, max_duration_seconds: int) -> tuple[str, ...]:
    violations: list[str] = []
    if not str(evidence.get("backup_id", "")).strip():
        violations.append("backup_identifier_is_required")
    last_success_at = evidence.get("backup_completed_at")
    if not isinstance(last_success_at, str):
        violations.append("backup_completion_timestamp_is_required")
    else:
        violations.extend(backup_rpo_violations(last_success_at=last_success_at, observed_at=observed_at, max_age_seconds=max_age_seconds))
    violations.extend(restore_rto_violations(evidence, max_duration_seconds=max_duration_seconds))
    return tuple(violations)


def recovery_evidence_is_ready(**inputs: object) -> bool:
    return not recovery_evidence_violations(**inputs)

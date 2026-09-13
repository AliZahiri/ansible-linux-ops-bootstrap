from __future__ import annotations

from datetime import datetime
import re
_SHA256=re.compile(r'sha256:[0-9a-f]{64}\Z')
def _time(value: object) -> datetime | None:
    if not isinstance(value,str): return None
    try: parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError: return None
    return parsed if parsed.tzinfo and parsed.utcoffset() is not None else None
def backup_restore_execution_violations(evidence: object, *, recovery_point_id: str, now: datetime, maximum_age_seconds: int=2592000) -> tuple[str,...]:
    if not isinstance(recovery_point_id,str) or not recovery_point_id.strip() or now.tzinfo is None or maximum_age_seconds<1: raise ValueError('invalid policy')
    if not isinstance(evidence,dict): return ('restore_evidence_must_be_an_object',)
    violations=[]
    if evidence.get('recovery_point_id')!=recovery_point_id: violations.append('recovery_point_must_match_approved_backup')
    if evidence.get('restore_succeeded') is not True: violations.append('restore_must_succeed')
    if evidence.get('isolated_destination') is not True: violations.append('restore_destination_must_be_isolated')
    if not isinstance(evidence.get('restored_sha256'),str) or not _SHA256.fullmatch(evidence['restored_sha256']): violations.append('restored_sha256_must_be_a_digest')
    observed=_time(evidence.get('observed_at'))
    if observed is None or not 0 <= (now-observed).total_seconds() <= maximum_age_seconds: violations.append('restore_evidence_is_invalid_stale_or_future_dated')
    return tuple(violations)

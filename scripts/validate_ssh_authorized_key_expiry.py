from __future__ import annotations

from datetime import datetime


def _time(value: object) -> datetime | None:
    if not isinstance(value, str): return None
    try: value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError: return None
    return value if value.tzinfo is not None and value.utcoffset() is not None else None


def ssh_authorized_key_expiry_violations(entries: object, *, now: datetime, maximum_lifetime_seconds: int = 31_536_000) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None or not isinstance(maximum_lifetime_seconds, int) or isinstance(maximum_lifetime_seconds, bool) or maximum_lifetime_seconds < 1: raise ValueError('invalid expiry policy')
    if not isinstance(entries, list) or not entries: return ('authorized_key_entries_must_be_a_non_empty_list',)
    violations: list[str] = []; seen: set[tuple[str, str]] = set()
    for position, entry in enumerate(entries):
        prefix = f'entry_{position}'
        if not isinstance(entry, dict): violations.append(f'{prefix}:entry_must_be_an_object'); continue
        account, fingerprint = entry.get('account'), entry.get('fingerprint')
        if not isinstance(account, str) or not account.strip() or not isinstance(fingerprint, str) or not fingerprint.strip(): violations.append(f'{prefix}:account_and_fingerprint_are_required')
        else:
            assignment = (account, fingerprint)
            if assignment in seen: violations.append(f'{prefix}:account_fingerprint_assignment_must_be_unique')
            seen.add(assignment)
        expires_at = _time(entry.get('expires_at'))
        if expires_at is None or not 0 < (expires_at - now).total_seconds() <= maximum_lifetime_seconds: violations.append(f'{prefix}:expiry_is_missing_expired_or_exceeds_maximum_lifetime')
    return tuple(violations)

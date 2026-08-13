from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def service_account_key_rotation_violations(records: list[dict[str, object]], *, now: datetime, maximum_age_days: int = 90) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_days, int) or isinstance(maximum_age_days, bool) or maximum_age_days <= 0:
        raise ValueError("maximum age days must be positive")
    if not records:
        return ("at_least_one_key_rotation_record_is_required",)
    violations: list[str] = []
    seen_accounts: set[str] = set()
    for index, record in enumerate(records):
        account = record.get("service_account")
        if not isinstance(account, str) or not account.strip():
            violations.append(f"record_{index}:service_account_is_required")
        elif account in seen_accounts:
            violations.append(f"record_{index}:service_account_must_be_unique")
        seen_accounts.add(account)
        if not isinstance(record.get("key_id"), str) or not record["key_id"].strip():
            violations.append(f"record_{index}:key_id_is_required")
        rotated_at, expires_at = _timestamp(record.get("rotated_at")), _timestamp(record.get("expires_at"))
        if rotated_at is None:
            violations.append(f"record_{index}:rotated_at_must_be_timezone_aware")
        elif not 0 <= (now - rotated_at).days <= maximum_age_days:
            violations.append(f"record_{index}:rotation_is_not_fresh")
        if expires_at is None or (expires_at - now).total_seconds() <= 0:
            violations.append(f"record_{index}:key_must_not_be_expired")
    return tuple(violations)


def service_account_key_rotation_is_current(records: list[dict[str, object]], **policy: object) -> bool:
    return not service_account_key_rotation_violations(records, **policy)

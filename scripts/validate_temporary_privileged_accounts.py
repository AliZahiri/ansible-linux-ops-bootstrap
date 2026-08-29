from __future__ import annotations

from datetime import datetime


def temporary_privileged_account_violations(accounts: list[dict[str, object]], *, now: datetime, maximum_validity_seconds: int = 86400) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_validity_seconds, int) or isinstance(maximum_validity_seconds, bool) or maximum_validity_seconds < 1:
        raise ValueError("maximum_validity_seconds must be a positive integer")
    if not isinstance(accounts, list) or not accounts:
        return ("at_least_one_temporary_privileged_account_is_required",)
    violations: list[str] = []
    seen_users: set[str] = set()
    for index, account in enumerate(accounts):
        if not isinstance(account, dict):
            violations.append(f"account_{index}:must_be_an_object")
            continue
        username = account.get("username")
        if not isinstance(username, str) or not username.strip():
            violations.append(f"account_{index}:username_is_required")
        elif username in seen_users:
            violations.append(f"account_{index}:username_must_be_unique")
        else:
            seen_users.add(username)
        for field in ("approval_ticket", "approved_by"):
            if not isinstance(account.get(field), str) or not account[field].strip():
                violations.append(f"account_{index}:{field}_is_required")
        if account.get("password_locked") is not True:
            violations.append(f"account_{index}:password_must_be_locked")
        key_count = account.get("ssh_key_count")
        if not isinstance(key_count, int) or isinstance(key_count, bool) or key_count < 1:
            violations.append(f"account_{index}:ssh_key_count_must_be_positive")
        expires_at = _timestamp(account.get("expires_at"))
        if expires_at is None:
            violations.append(f"account_{index}:expires_at_must_be_timezone_aware")
        else:
            remaining = (expires_at - now).total_seconds()
            if remaining <= 0:
                violations.append(f"account_{index}:temporary_access_is_expired")
            elif remaining > maximum_validity_seconds:
                violations.append(f"account_{index}:temporary_access_exceeds_validity_window")
    return tuple(violations)


def temporary_privileged_accounts_are_safe(accounts: list[dict[str, object]], **policy: object) -> bool:
    return not temporary_privileged_account_violations(accounts, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

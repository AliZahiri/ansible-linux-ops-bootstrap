from __future__ import annotations

from datetime import datetime
import re


_FINGERPRINT = re.compile(r"SHA256:[A-Za-z0-9+/]{43}=?\Z")
_TICKET = re.compile(r"[A-Z][A-Z0-9]+-[1-9][0-9]*\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def ssh_authorized_key_provenance_violations(
    entries: object, *, now: datetime, maximum_review_age_seconds: int = 7_776_000
) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    if not isinstance(maximum_review_age_seconds, int) or isinstance(maximum_review_age_seconds, bool) or maximum_review_age_seconds < 1:
        raise ValueError("maximum_review_age_seconds must be a positive integer")
    if not isinstance(entries, list) or not entries:
        return ("authorized_key_entries_must_be_a_non_empty_list",)

    violations: list[str] = []
    seen_assignments: set[tuple[str, str]] = set()
    for position, entry in enumerate(entries):
        prefix = f"entry_{position}"
        if not isinstance(entry, dict):
            violations.append(f"{prefix}:entry_must_be_an_object")
            continue
        account = entry.get("account")
        fingerprint = entry.get("fingerprint")
        if not isinstance(account, str) or not account.strip() or account == "root":
            violations.append(f"{prefix}:account_must_be_a_non_root_identity")
        if not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint):
            violations.append(f"{prefix}:fingerprint_must_be_an_openssh_sha256_value")
        elif isinstance(account, str) and account.strip():
            assignment = (account, fingerprint)
            if assignment in seen_assignments:
                violations.append(f"{prefix}:account_fingerprint_assignment_must_be_unique")
            seen_assignments.add(assignment)
        if not isinstance(entry.get("change_ticket"), str) or not _TICKET.fullmatch(entry["change_ticket"]):
            violations.append(f"{prefix}:change_ticket_is_invalid")
        reviewed_at = _timestamp(entry.get("reviewed_at"))
        if reviewed_at is None:
            violations.append(f"{prefix}:reviewed_at_must_be_timezone_aware")
        else:
            age = (now - reviewed_at).total_seconds()
            if age < 0 or age > maximum_review_age_seconds:
                violations.append(f"{prefix}:review_is_stale_or_future_dated")
    return tuple(violations)


def ssh_authorized_key_provenance_is_current(entries: object, **policy: object) -> bool:
    return not ssh_authorized_key_provenance_violations(entries, **policy)

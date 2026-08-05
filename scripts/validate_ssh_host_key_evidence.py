from __future__ import annotations

from datetime import datetime
import re


_FINGERPRINT = re.compile(r"SHA256:[A-Za-z0-9+/]{43}=?\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def ssh_host_key_evidence_violations(hosts: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 2592000) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be a positive integer")
    if not hosts:
        return ("at_least_one_host_key_observation_is_required",)
    violations: list[str] = []
    seen_hosts: set[str] = set()
    for position, host in enumerate(hosts):
        name = str(host.get("host", "")).strip().lower()
        if not name:
            violations.append(f"host_{position}:host_is_required")
        elif name in seen_hosts:
            violations.append(f"host_{position}:host_must_be_unique")
        seen_hosts.add(name)
        if host.get("strict_host_key_checking") is not True:
            violations.append(f"host_{position}:strict_host_key_checking_must_be_enabled")
        fingerprint = host.get("fingerprint")
        if not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint):
            violations.append(f"host_{position}:fingerprint_must_be_an_openssh_sha256_value")
        verified_at = _timestamp(host.get("verified_at"))
        if verified_at is None:
            violations.append(f"host_{position}:verified_at_must_be_timezone_aware")
            continue
        age = (now - verified_at).total_seconds()
        if age < 0:
            violations.append(f"host_{position}:host_key_verification_is_in_the_future")
        elif age > maximum_age_seconds:
            violations.append(f"host_{position}:host_key_verification_is_stale")
    return tuple(violations)


def ssh_host_key_evidence_is_current(hosts: list[dict[str, object]], **policy: object) -> bool:
    return not ssh_host_key_evidence_violations(hosts, **policy)

from __future__ import annotations

from datetime import datetime
import re


_FINGERPRINT = re.compile(r"[A-F0-9]{40}(?:[A-F0-9]{24})?\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def apt_repository_trust_violations(repositories: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 2592000) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be a positive integer")
    if not repositories:
        return ("at_least_one_repository_observation_is_required",)

    violations: list[str] = []
    seen_names: set[str] = set()
    for index, repository in enumerate(repositories):
        name = str(repository.get("name", "")).strip().lower()
        if not name:
            violations.append(f"repository_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"repository_{index}:name_must_be_unique")
        seen_names.add(name)
        signed_by = repository.get("signed_by")
        if not isinstance(signed_by, str) or not signed_by.startswith("/etc/apt/keyrings/") or ".." in signed_by.split("/"):
            violations.append(f"repository_{index}:signed_by_must_use_dedicated_keyring")
        fingerprint = repository.get("fingerprint")
        if not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint.upper()):
            violations.append(f"repository_{index}:fingerprint_must_be_a_valid_openpgp_value")
        if repository.get("signature_verified") is not True:
            violations.append(f"repository_{index}:signature_must_be_verified")
        verified_at = _timestamp(repository.get("verified_at"))
        if verified_at is None:
            violations.append(f"repository_{index}:verified_at_must_be_timezone_aware")
            continue
        age = (now - verified_at).total_seconds()
        if age < 0 or age > maximum_age_seconds:
            violations.append(f"repository_{index}:trust_evidence_is_not_fresh")
    return tuple(violations)


def apt_repository_trust_is_current(repositories: list[dict[str, object]], **policy: object) -> bool:
    return not apt_repository_trust_violations(repositories, **policy)

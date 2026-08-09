from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def sudoers_evidence_violations(files: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 86400) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be a positive integer")
    if not files:
        return ("at_least_one_sudoers_observation_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, item in enumerate(files):
        path = str(item.get("path", "")).strip()
        if not path.startswith("/etc/sudoers.d/") or ".." in path.split("/"):
            violations.append(f"file_{position}:path_must_be_a_sudoers_fragment")
        elif path in seen:
            violations.append(f"file_{position}:path_must_be_unique")
        seen.add(path)
        if item.get("owner") != "root" or item.get("group") != "root":
            violations.append(f"file_{position}:ownership_must_be_root_root")
        if item.get("mode") != "0440":
            violations.append(f"file_{position}:mode_must_be_0440")
        digest = item.get("sha256")
        if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
            violations.append(f"file_{position}:sha256_is_invalid")
        if item.get("visudo_check_passed") is not True:
            violations.append(f"file_{position}:visudo_check_must_pass")
        verified_at = _timestamp(item.get("verified_at"))
        if verified_at is None:
            violations.append(f"file_{position}:verified_at_must_be_timezone_aware")
            continue
        age = (now - verified_at).total_seconds()
        if age < 0 or age > maximum_age_seconds:
            violations.append(f"file_{position}:verification_is_not_fresh")
    return tuple(violations)


def sudoers_evidence_is_safe(files: list[dict[str, object]], **policy: object) -> bool:
    return not sudoers_evidence_violations(files, **policy)

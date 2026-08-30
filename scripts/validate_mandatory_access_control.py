from __future__ import annotations

from datetime import datetime


_FRAMEWORKS = frozenset({"selinux", "apparmor"})


def mandatory_access_control_violations(hosts: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 86400) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be a positive integer")
    if not isinstance(hosts, list) or not hosts:
        return ("at_least_one_host_is_required",)
    violations: list[str] = []
    seen_hosts: set[str] = set()
    for index, host in enumerate(hosts):
        if not isinstance(host, dict):
            violations.append(f"host_{index}:must_be_an_object")
            continue
        hostname = host.get("hostname")
        if not isinstance(hostname, str) or not hostname.strip():
            violations.append(f"host_{index}:hostname_is_required")
        elif hostname in seen_hosts:
            violations.append(f"host_{index}:hostname_must_be_unique")
        else:
            seen_hosts.add(hostname)
        if host.get("framework") not in _FRAMEWORKS:
            violations.append(f"host_{index}:framework_must_be_selinux_or_apparmor")
        if host.get("mode") != "enforcing":
            violations.append(f"host_{index}:mode_must_be_enforcing")
        if not isinstance(host.get("policy_name"), str) or not host["policy_name"].strip():
            violations.append(f"host_{index}:policy_name_is_required")
        profile_count = host.get("enforced_profile_count")
        if not isinstance(profile_count, int) or isinstance(profile_count, bool) or profile_count < 1:
            violations.append(f"host_{index}:enforced_profile_count_must_be_positive")
        if host.get("denial_events_reviewed") is not True:
            violations.append(f"host_{index}:denial_events_must_be_reviewed")
        observed_at = _timestamp(host.get("observed_at"))
        if observed_at is None:
            violations.append(f"host_{index}:observed_at_must_be_timezone_aware")
        else:
            age = (now - observed_at).total_seconds()
            if age < 0:
                violations.append(f"host_{index}:observation_must_not_be_in_the_future")
            elif age > maximum_age_seconds:
                violations.append(f"host_{index}:observation_is_stale")
    return tuple(violations)


def mandatory_access_control_is_enforced(hosts: list[dict[str, object]], **policy: object) -> bool:
    return not mandatory_access_control_violations(hosts, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

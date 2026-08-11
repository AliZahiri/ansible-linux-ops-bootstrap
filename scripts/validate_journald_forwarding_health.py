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


def journald_forwarding_health_violations(observations: list[dict[str, object]], *, now: datetime, maximum_age_seconds: int = 900) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be positive")
    if not observations:
        return ("at_least_one_forwarding_observation_is_required",)
    violations: list[str] = []
    seen_hosts: set[str] = set()
    for index, observation in enumerate(observations):
        host = observation.get("host")
        if not isinstance(host, str) or not host.strip():
            violations.append(f"observation_{index}:host_is_required")
        elif host in seen_hosts:
            violations.append(f"observation_{index}:host_must_be_unique")
        seen_hosts.add(host)
        if observation.get("forwarding_enabled") is not True:
            violations.append(f"observation_{index}:forwarding_must_be_enabled")
        delivered_at = _timestamp(observation.get("delivered_at"))
        if delivered_at is None or (now - delivered_at).total_seconds() < 0 or (now - delivered_at).total_seconds() > maximum_age_seconds:
            violations.append(f"observation_{index}:delivery_is_not_fresh")
        backlog = observation.get("backlog_count")
        if not isinstance(backlog, int) or isinstance(backlog, bool) or backlog < 0:
            violations.append(f"observation_{index}:backlog_count_must_be_non_negative")
    return tuple(violations)


def journald_forwarding_is_healthy(observations: list[dict[str, object]], **policy: object) -> bool:
    return not journald_forwarding_health_violations(observations, **policy)

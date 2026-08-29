from __future__ import annotations

from datetime import datetime
from math import isfinite


def dns_resolver_health_violations(hosts: list[dict[str, object]], *, now: datetime, minimum_nameservers: int = 2, maximum_age_seconds: int = 300, maximum_latency_ms: float = 1000.0) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    for name, value in (("minimum_nameservers", minimum_nameservers), ("maximum_age_seconds", maximum_age_seconds)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if not _finite_non_negative(maximum_latency_ms) or maximum_latency_ms == 0:
        raise ValueError("maximum_latency_ms must be positive and finite")
    if not isinstance(hosts, list) or not hosts:
        return ("at_least_one_dns_observation_is_required",)
    violations: list[str] = []
    seen_hosts: set[str] = set()
    for index, host in enumerate(hosts):
        if not isinstance(host, dict):
            violations.append(f"host_{index}:must_be_an_object")
            continue
        host_id = host.get("host_id")
        if not isinstance(host_id, str) or not host_id.strip():
            violations.append(f"host_{index}:host_id_is_required")
        elif host_id in seen_hosts:
            violations.append(f"host_{index}:host_id_must_be_unique")
        else:
            seen_hosts.add(host_id)
        nameservers = host.get("nameservers")
        if not isinstance(nameservers, list) or len(nameservers) < minimum_nameservers or any(not isinstance(item, str) or not item.strip() for item in nameservers):
            violations.append(f"host_{index}:nameserver_coverage_is_below_minimum")
        elif len(set(nameservers)) != len(nameservers):
            violations.append(f"host_{index}:nameservers_must_be_unique")
        observed_at = _timestamp(host.get("observed_at"))
        if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
            violations.append(f"host_{index}:observation_is_stale_or_invalid")
        if host.get("lookup_succeeded") is not True:
            violations.append(f"host_{index}:dns_lookup_must_succeed")
        latency = host.get("resolution_latency_ms")
        if not _finite_non_negative(latency):
            violations.append(f"host_{index}:resolution_latency_ms_must_be_finite_and_non_negative")
        elif latency > maximum_latency_ms:
            violations.append(f"host_{index}:resolution_latency_exceeds_budget")
    return tuple(violations)


def dns_resolvers_are_healthy(hosts: list[dict[str, object]], **policy: object) -> bool:
    return not dns_resolver_health_violations(hosts, **policy)


def _finite_non_negative(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(float(value)) and value >= 0


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

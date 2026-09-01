from __future__ import annotations

from datetime import datetime


def firewall_ruleset_drift_violations(expected_services: list[str], observation: dict[str, object], *, now: datetime, maximum_age_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be a positive integer")
    if not isinstance(expected_services, list) or any(not isinstance(item, str) or not item.strip() for item in expected_services):
        raise ValueError("expected_services must be a string list")
    violations: list[str] = []
    if len(set(expected_services)) != len(expected_services):
        violations.append("expected_services_must_be_unique")
    if observation.get("default_input_policy") not in {"drop", "reject"}:
        violations.append("default_input_policy_must_deny")
    observed = observation.get("allowed_services")
    if not isinstance(observed, list) or any(not isinstance(item, str) or not item.strip() for item in observed):
        violations.append("allowed_services_must_be_a_string_list")
    else:
        expected_set = set(expected_services)
        observed_set = set(observed)
        if expected_set - observed_set:
            violations.append("required_firewall_services_are_missing")
        if observed_set - expected_set:
            violations.append("unexpected_firewall_services_are_allowed")
    captured_at = _timestamp(observation.get("captured_at"))
    if captured_at is None:
        violations.append("captured_at_must_be_timezone_aware")
    elif not 0 <= (now - captured_at).total_seconds() <= maximum_age_seconds:
        violations.append("firewall_observation_is_stale_or_future_dated")
    if not isinstance(observation.get("ruleset_digest"), str) or not observation["ruleset_digest"].strip():
        violations.append("ruleset_digest_is_required")
    return tuple(violations)


def firewall_ruleset_matches(expected_services: list[str], observation: dict[str, object], **policy: object) -> bool:
    return not firewall_ruleset_drift_violations(expected_services, observation, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

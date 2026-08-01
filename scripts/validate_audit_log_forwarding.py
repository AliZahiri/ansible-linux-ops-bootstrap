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


def audit_log_forwarding_violations(evidence: dict[str, object], *, now: datetime, maximum_delivery_age_seconds: int = 300) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_delivery_age_seconds, int) or isinstance(maximum_delivery_age_seconds, bool) or maximum_delivery_age_seconds <= 0:
        raise ValueError("maximum delivery age must be a positive integer")
    violations: list[str] = []
    if evidence.get("service_active") is not True:
        violations.append("audit_forwarder_service_must_be_active")
    if evidence.get("tls_peer_verified") is not True:
        violations.append("audit_forwarder_tls_peer_must_be_verified")
    if evidence.get("disk_queue_enabled") is not True:
        violations.append("audit_forwarder_disk_queue_must_be_enabled")
    destinations = evidence.get("destination_count")
    if not isinstance(destinations, int) or isinstance(destinations, bool) or destinations <= 0:
        violations.append("audit_forwarder_destination_is_required")
    dropped = evidence.get("dropped_events")
    if not isinstance(dropped, int) or isinstance(dropped, bool) or dropped < 0:
        violations.append("dropped_event_count_must_be_non_negative")
    elif dropped > 0:
        violations.append("audit_events_must_not_be_dropped")
    delivered_at = _timestamp(evidence.get("last_delivery_at"))
    if delivered_at is None:
        violations.append("last_delivery_at_must_be_timezone_aware")
    else:
        age = (now - delivered_at).total_seconds()
        if age < 0:
            violations.append("audit_delivery_observation_is_in_the_future")
        elif age > maximum_delivery_age_seconds:
            violations.append("audit_delivery_observation_is_stale")
    return tuple(violations)


def audit_log_forwarding_is_ready(evidence: dict[str, object], **policy: object) -> bool:
    return not audit_log_forwarding_violations(evidence, **policy)

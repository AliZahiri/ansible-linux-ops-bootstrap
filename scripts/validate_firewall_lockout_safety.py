from __future__ import annotations

from datetime import datetime
from ipaddress import ip_network


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def firewall_lockout_violations(evidence: dict[str, object], *, now: datetime, maximum_rollback_window_seconds: int = 600) -> tuple[str, ...]:
    if not isinstance(maximum_rollback_window_seconds, int) or isinstance(maximum_rollback_window_seconds, bool) or maximum_rollback_window_seconds <= 0:
        raise ValueError("maximum rollback window must be a positive integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    violations: list[str] = []
    source = evidence.get("management_source_cidr")
    try:
        ip_network(str(source), strict=False)
    except ValueError:
        violations.append("management_source_cidr_is_invalid")
    port = evidence.get("ssh_port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        violations.append("ssh_port_is_invalid")
    if evidence.get("established_session_confirmed") is not True:
        violations.append("established_management_session_must_be_confirmed")
    if evidence.get("policy_validation_passed") is not True:
        violations.append("firewall_policy_validation_must_pass")
    if not str(evidence.get("rollback_job_id", "")).strip():
        violations.append("rollback_job_id_is_required")
    deadline = _timestamp(evidence.get("rollback_deadline"))
    if deadline is None:
        violations.append("rollback_deadline_must_be_timezone_aware")
    else:
        remaining = (deadline - now).total_seconds()
        if remaining <= 0:
            violations.append("rollback_deadline_must_be_in_the_future")
        elif remaining > maximum_rollback_window_seconds:
            violations.append("rollback_window_exceeds_maximum")
    return tuple(violations)


def firewall_change_is_lockout_safe(evidence: dict[str, object], **policy: object) -> bool:
    return not firewall_lockout_violations(evidence, **policy)

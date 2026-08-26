from __future__ import annotations

from datetime import datetime


def host_batch_failure_budget_violations(summary: dict[str, object], *, max_failed: int = 0, max_unreachable: int = 0) -> tuple[str, ...]:
    for name, value in (("max_failed", max_failed), ("max_unreachable", max_unreachable)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    violations: list[str] = []
    if not isinstance(summary.get("batch_id"), str) or not summary["batch_id"].strip():
        violations.append("batch_id_is_required")
    hosts = summary.get("hosts")
    if not isinstance(hosts, int) or isinstance(hosts, bool) or hosts < 1:
        violations.append("hosts_must_be_positive")
    for field, budget in (("failed", max_failed), ("unreachable", max_unreachable)):
        value = summary.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            violations.append(f"{field}_must_be_non_negative")
        elif value > budget:
            violations.append(f"{field}_hosts_exceed_budget")
    if _timestamp(summary.get("completed_at")) is None:
        violations.append("completed_at_must_be_timezone_aware")
    return tuple(violations)


def host_batch_is_within_failure_budget(summary: dict[str, object], **policy: object) -> bool:
    return not host_batch_failure_budget_violations(summary, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

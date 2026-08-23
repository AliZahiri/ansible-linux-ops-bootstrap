from __future__ import annotations

from datetime import datetime


def check_mode_change_budget_violations(report: dict[str, object], *, max_changed: int = 10) -> tuple[str, ...]:
    if not isinstance(max_changed, int) or isinstance(max_changed, bool) or max_changed < 0:
        raise ValueError("max_changed must be a non-negative integer")
    violations: list[str] = []
    hosts = report.get("hosts")
    if not isinstance(hosts, int) or isinstance(hosts, bool) or hosts < 1:
        violations.append("hosts_must_be_positive")
    for field in ("failed", "unreachable", "changed"):
        value = report.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            violations.append(f"{field}_must_be_non_negative")
    if isinstance(report.get("failed"), int) and report["failed"] > 0:
        violations.append("check_mode_must_have_no_failures")
    if isinstance(report.get("unreachable"), int) and report["unreachable"] > 0:
        violations.append("check_mode_must_have_no_unreachable_hosts")
    if isinstance(report.get("changed"), int) and report["changed"] > max_changed:
        violations.append("changed_count_exceeds_budget")
    if _timestamp(report.get("checked_at")) is None:
        violations.append("checked_at_must_be_timezone_aware")
    return tuple(violations)


def check_mode_change_budget_is_safe(report: dict[str, object], *, max_changed: int = 10) -> bool:
    return not check_mode_change_budget_violations(report, max_changed=max_changed)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

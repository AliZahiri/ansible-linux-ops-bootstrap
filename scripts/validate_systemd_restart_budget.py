from __future__ import annotations

from datetime import datetime


def systemd_restart_budget_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("restart_budget", "observation_window_minutes"):
        value = evidence.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            violations.append(f"{field}_must_be_positive")
    observed = evidence.get("observed_restarts")
    if not isinstance(observed, int) or isinstance(observed, bool) or observed < 0:
        violations.append("observed_restarts_must_be_non_negative")
    elif isinstance(evidence.get("restart_budget"), int) and not isinstance(evidence["restart_budget"], bool) and observed > evidence["restart_budget"]:
        violations.append("observed_restarts_exceed_budget")
    if evidence.get("unit_active") is not True:
        violations.append("unit_must_be_active")
    if _parse_timestamp(evidence.get("observed_at")) is None:
        violations.append("observed_at_must_be_timezone_aware")
    return tuple(violations)


def systemd_restart_budget_is_healthy(evidence: dict[str, object]) -> bool:
    return not systemd_restart_budget_violations(evidence)


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

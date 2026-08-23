from __future__ import annotations

from datetime import datetime


def kernel_parameter_drift_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    parameters = evidence.get("parameters")
    if not isinstance(parameters, list) or not parameters:
        return ("at_least_one_kernel_parameter_is_required",)
    seen: set[str] = set()
    for index, item in enumerate(parameters):
        if not isinstance(item, dict):
            violations.append(f"parameter_{index}:must_be_an_object")
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"parameter_{index}:name_is_required")
        elif name in seen:
            violations.append(f"parameter_{index}:name_must_be_unique")
        else:
            seen.add(name)
        if item.get("expected") != item.get("observed"):
            violations.append(f"parameter_{index}:runtime_value_drifted")
    if evidence.get("reboot_required") is True:
        violations.append("reboot_is_required_for_kernel_convergence")
    if _timestamp(evidence.get("observed_at")) is None:
        violations.append("observed_at_must_be_timezone_aware")
    return tuple(violations)


def kernel_parameters_are_converged(evidence: dict[str, object]) -> bool:
    return not kernel_parameter_drift_violations(evidence)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

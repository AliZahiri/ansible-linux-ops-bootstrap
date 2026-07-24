from __future__ import annotations


_RECAP_METRICS = ("changed", "failed", "unreachable")


def _recap_violations(label: str, recap: dict[str, object]) -> list[str]:
    if not recap:
        return [f"{label}:recap_is_required"]
    violations: list[str] = []
    for host in sorted(recap):
        metrics = recap[host]
        if not isinstance(metrics, dict):
            violations.append(f"{label}:{host}:metrics_must_be_an_object")
            continue
        for metric in _RECAP_METRICS:
            value = metrics.get(metric)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                violations.append(f"{label}:{host}:{metric}_must_be_a_non_negative_integer")
            elif metric in {"failed", "unreachable"} and value:
                violations.append(f"{label}:{host}:{metric}_must_be_zero")
            elif label == "verification" and metric == "changed" and value:
                violations.append(f"{label}:{host}:changed_must_be_zero")
    return violations


def idempotency_violations(*, first_run: dict[str, object], verification_run: dict[str, object]) -> tuple[str, ...]:
    violations = _recap_violations("first", first_run)
    violations.extend(_recap_violations("verification", verification_run))
    if first_run and verification_run and set(first_run) != set(verification_run):
        violations.append("run_host_sets_must_match")
    return tuple(violations)


def idempotency_is_proven(*, first_run: dict[str, object], verification_run: dict[str, object]) -> bool:
    return not idempotency_violations(first_run=first_run, verification_run=verification_run)

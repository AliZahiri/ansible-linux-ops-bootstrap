from __future__ import annotations

from math import isfinite


def time_sync_health_violations(evidence: dict[str, object], *, maximum_absolute_offset_ms: float = 100.0) -> tuple[str, ...]:
    if not isinstance(maximum_absolute_offset_ms, (int, float)) or isinstance(maximum_absolute_offset_ms, bool) or not isfinite(float(maximum_absolute_offset_ms)) or maximum_absolute_offset_ms <= 0:
        raise ValueError("maximum absolute offset must be positive and finite")
    violations: list[str] = []
    if evidence.get("synchronized") is not True:
        violations.append("clock_must_be_synchronized")
    sources = evidence.get("usable_source_count")
    if not isinstance(sources, int) or isinstance(sources, bool) or sources <= 0:
        violations.append("at_least_one_usable_time_source_is_required")
    stratum = evidence.get("stratum")
    if not isinstance(stratum, int) or isinstance(stratum, bool) or not 1 <= stratum <= 15:
        violations.append("stratum_must_be_between_1_and_15")
    offset = evidence.get("offset_ms")
    if not isinstance(offset, (int, float)) or isinstance(offset, bool) or not isfinite(float(offset)):
        violations.append("clock_offset_must_be_finite")
    elif abs(float(offset)) > maximum_absolute_offset_ms:
        violations.append("clock_offset_exceeds_maximum")
    if evidence.get("leap_status") != "normal":
        violations.append("leap_status_must_be_normal")
    return tuple(violations)


def time_sync_is_healthy(evidence: dict[str, object], **policy: object) -> bool:
    return not time_sync_health_violations(evidence, **policy)

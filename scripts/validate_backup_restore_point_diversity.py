from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def backup_restore_point_diversity_violations(points: list[dict[str, object]], *, now: datetime, minimum_points: int = 3, maximum_age_days: int = 14) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(minimum_points, int) or isinstance(minimum_points, bool) or minimum_points < 2:
        raise ValueError("minimum points must be at least two")
    if not isinstance(maximum_age_days, int) or isinstance(maximum_age_days, bool) or maximum_age_days <= 0:
        raise ValueError("maximum age days must be positive")
    violations: list[str] = []
    if len(points) < minimum_points:
        violations.append("minimum_restore_point_count_is_not_met")
    seen_ids: set[str] = set()
    for index, point in enumerate(points):
        point_id = point.get("backup_id")
        if not isinstance(point_id, str) or not point_id.strip():
            violations.append(f"point_{index}:backup_id_is_required")
        elif point_id in seen_ids:
            violations.append(f"point_{index}:backup_id_must_be_unique")
        if isinstance(point_id, str):
            seen_ids.add(point_id)
        if not isinstance(point.get("sha256"), str) or not _SHA256.fullmatch(point["sha256"]):
            violations.append(f"point_{index}:sha256_is_invalid")
        created_at = _timestamp(point.get("created_at"))
        if created_at is None or not 0 <= (now - created_at).days <= maximum_age_days:
            violations.append(f"point_{index}:restore_point_is_not_within_age_budget")
    return tuple(violations)


def backup_restore_points_are_diverse(points: list[dict[str, object]], **policy: object) -> bool:
    return not backup_restore_point_diversity_violations(points, **policy)

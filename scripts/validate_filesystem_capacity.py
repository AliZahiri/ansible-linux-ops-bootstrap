from __future__ import annotations

from math import isfinite


def filesystem_capacity_violations(filesystems: list[dict[str, object]], *, maximum_used_percent: float = 85.0, maximum_inode_used_percent: float = 85.0) -> tuple[str, ...]:
    for name, value in (("maximum used percent", maximum_used_percent), ("maximum inode used percent", maximum_inode_used_percent)):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(float(value)) or not 0 < value < 100:
            raise ValueError(f"{name} must be finite and between zero and 100")
    if not filesystems:
        return ("at_least_one_filesystem_observation_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, filesystem in enumerate(filesystems):
        mount = str(filesystem.get("mount", "")).strip()
        if not mount.startswith("/"):
            violations.append(f"filesystem_{position}:mount_must_be_absolute")
        elif mount in seen:
            violations.append(f"filesystem_{position}:mount_must_be_unique")
        seen.add(mount)
        if filesystem.get("writable") is not True:
            violations.append(f"filesystem_{position}:mount_must_be_writable")
        for field, maximum in (("used_percent", maximum_used_percent), ("inode_used_percent", maximum_inode_used_percent)):
            value = filesystem.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(float(value)) or not 0 <= value <= 100:
                violations.append(f"filesystem_{position}:{field}_must_be_between_zero_and_100")
            elif value > maximum:
                violations.append(f"filesystem_{position}:{field}_exceeds_maximum")
    return tuple(violations)

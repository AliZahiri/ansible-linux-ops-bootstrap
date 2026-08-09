from __future__ import annotations


_ALLOWED_FREQUENCIES = {"daily", "weekly"}


def logrotate_policy_violations(policies: list[dict[str, object]], *, minimum_rotations: int = 7, maximum_size_mb: int = 1024) -> tuple[str, ...]:
    if not isinstance(minimum_rotations, int) or isinstance(minimum_rotations, bool) or minimum_rotations <= 0:
        raise ValueError("minimum rotations must be a positive integer")
    if not isinstance(maximum_size_mb, int) or isinstance(maximum_size_mb, bool) or maximum_size_mb <= 0:
        raise ValueError("maximum size must be a positive integer")
    if not policies:
        return ("at_least_one_logrotate_policy_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, policy in enumerate(policies):
        path = str(policy.get("path", "")).strip()
        if not path.startswith("/") or ".." in path.split("/"):
            violations.append(f"policy_{position}:path_must_be_absolute")
        elif path in seen:
            violations.append(f"policy_{position}:path_must_be_unique")
        seen.add(path)
        if policy.get("frequency") not in _ALLOWED_FREQUENCIES:
            violations.append(f"policy_{position}:frequency_is_invalid")
        rotations = policy.get("rotations")
        if not isinstance(rotations, int) or isinstance(rotations, bool) or rotations < minimum_rotations:
            violations.append(f"policy_{position}:rotations_below_minimum")
        size_mb = policy.get("size_mb")
        if not isinstance(size_mb, int) or isinstance(size_mb, bool) or not 0 < size_mb <= maximum_size_mb:
            violations.append(f"policy_{position}:size_mb_is_invalid")
        if policy.get("compress") is not True:
            violations.append(f"policy_{position}:compression_must_be_enabled")
        mechanisms = int(policy.get("copytruncate") is True) + int(policy.get("postrotate_reload") is True)
        if mechanisms != 1:
            violations.append(f"policy_{position}:exactly_one_reopen_strategy_is_required")
    return tuple(violations)


def logrotate_policy_is_safe(policies: list[dict[str, object]], **policy: object) -> bool:
    return not logrotate_policy_violations(policies, **policy)

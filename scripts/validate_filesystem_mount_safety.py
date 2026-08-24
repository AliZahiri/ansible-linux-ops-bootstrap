from __future__ import annotations

from pathlib import PurePosixPath


def filesystem_mount_safety_violations(mounts: list[dict[str, object]], required_options: dict[str, set[str]]) -> tuple[str, ...]:
    if not mounts:
        return ("at_least_one_mount_is_required",)
    violations: list[str] = []
    seen_targets: set[str] = set()
    for index, mount in enumerate(mounts):
        target, fstype, options = mount.get("target"), mount.get("fstype"), mount.get("options")
        if not isinstance(target, str) or not PurePosixPath(target).is_absolute():
            violations.append(f"mount_{index}:target_must_be_absolute")
            continue
        if target in seen_targets:
            violations.append(f"mount_{index}:target_must_be_unique")
        seen_targets.add(target)
        if not isinstance(fstype, str) or not fstype.strip():
            violations.append(f"mount_{index}:fstype_is_required")
        if not isinstance(options, list) or any(not isinstance(item, str) or not item.strip() for item in options):
            violations.append(f"mount_{index}:options_must_be_a_string_list")
            continue
        missing = required_options.get(target, set()) - set(options)
        for option in sorted(missing):
            violations.append(f"mount_{index}:required_option_{option}_is_missing")
    if "/" not in seen_targets:
        violations.append("root_mount_is_required")
    return tuple(violations)


def filesystem_mounts_are_safe(mounts: list[dict[str, object]], required_options: dict[str, set[str]]) -> bool:
    return not filesystem_mount_safety_violations(mounts, required_options)

from __future__ import annotations

import re


_VERSION = re.compile(r"=\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\Z")
_NAME = re.compile(r"[a-z0-9_]+\.[a-z0-9_]+\Z", re.IGNORECASE)


def collection_version_lock_violations(collections: list[dict[str, object]]) -> tuple[str, ...]:
    if not collections:
        return ("at_least_one_collection_lock_is_required",)
    violations: list[str] = []
    seen_names: set[str] = set()
    for index, collection in enumerate(collections):
        name = collection.get("name")
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            violations.append(f"collection_{index}:name_is_invalid")
            continue
        normalized = name.lower()
        if normalized in seen_names:
            violations.append(f"collection_{index}:name_must_be_unique")
        seen_names.add(normalized)
        version = collection.get("version")
        if not isinstance(version, str) or not _VERSION.fullmatch(version):
            violations.append(f"collection_{index}:version_must_be_exact_semver_pin")
        source = collection.get("source")
        if not isinstance(source, str) or not source.startswith("https://"):
            violations.append(f"collection_{index}:source_must_be_https")
    return tuple(violations)


def collection_version_lock_is_safe(collections: list[dict[str, object]]) -> bool:
    return not collection_version_lock_violations(collections)

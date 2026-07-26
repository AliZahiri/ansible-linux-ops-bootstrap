from __future__ import annotations

import re

from scripts.validate_backup_manifest import backup_manifest_violations


_SHA256 = re.compile(r"[a-fA-F0-9]{64}\Z")


def backup_observation_violations(*, manifest: dict[str, object], observed_size_bytes: object, observed_sha256: object) -> tuple[str, ...]:
    violations = [f"manifest:{item}" for item in backup_manifest_violations(manifest)]
    valid_size = isinstance(observed_size_bytes, int) and not isinstance(observed_size_bytes, bool) and observed_size_bytes > 0
    if not valid_size:
        violations.append("observed_size_bytes_must_be_a_positive_integer")
    elif isinstance(manifest.get("size_bytes"), int) and observed_size_bytes != manifest["size_bytes"]:
        violations.append("observed_size_does_not_match_manifest")
    valid_digest = isinstance(observed_sha256, str) and _SHA256.fullmatch(observed_sha256) is not None
    if not valid_digest:
        violations.append("observed_sha256_must_be_a_complete_digest")
    elif isinstance(manifest.get("sha256"), str) and observed_sha256.lower() != manifest["sha256"].lower():
        violations.append("observed_sha256_does_not_match_manifest")
    return tuple(violations)


def backup_observation_matches_manifest(**inputs: object) -> bool:
    return not backup_observation_violations(**inputs)

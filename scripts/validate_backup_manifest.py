from __future__ import annotations

from datetime import datetime
import re


_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256 = re.compile(r"[a-fA-F0-9]{64}\Z")


def _is_timezone_aware(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def backup_manifest_violations(manifest: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    backup_id = manifest.get("backup_id")
    if not isinstance(backup_id, str) or not _IDENTIFIER.fullmatch(backup_id):
        violations.append("backup_id_is_invalid")
    artifact_name = manifest.get("artifact_name")
    if not isinstance(artifact_name, str) or not artifact_name.strip() or "/" in artifact_name or "\\" in artifact_name:
        violations.append("artifact_name_must_not_contain_a_path")
    if not _is_timezone_aware(manifest.get("created_at")):
        violations.append("created_at_must_be_timezone_aware")
    size_bytes = manifest.get("size_bytes")
    if not isinstance(size_bytes, int) or isinstance(size_bytes, bool) or size_bytes <= 0:
        violations.append("size_bytes_must_be_a_positive_integer")
    digest = manifest.get("sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("sha256_must_be_a_complete_digest")
    return tuple(violations)


def backup_manifest_is_valid(manifest: dict[str, object]) -> bool:
    return not backup_manifest_violations(manifest)

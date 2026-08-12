from __future__ import annotations

import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_DEFAULT_ROOTS = ("/etc/ssh", "/etc/sudoers.d", "/etc/ssl/private")
_ALLOWED_MODES = {"0400", "0440", "0600", "0640"}


def _under_root(path: str, roots: tuple[str, ...]) -> bool:
    return any(path.startswith(root + "/") for root in roots)


def sensitive_file_contract_violations(files: list[dict[str, object]], *, allowed_roots: tuple[str, ...] = _DEFAULT_ROOTS) -> tuple[str, ...]:
    if not allowed_roots or not all(isinstance(root, str) and root.startswith("/") and root.rstrip("/") == root for root in allowed_roots):
        raise ValueError("allowed roots must be absolute paths without trailing slashes")
    if not files:
        return ("at_least_one_sensitive_file_is_required",)

    violations: list[str] = []
    seen_paths: set[str] = set()
    for index, item in enumerate(files):
        path = item.get("path")
        if not isinstance(path, str) or not _under_root(path, allowed_roots):
            violations.append(f"file_{index}:path_must_be_under_an_allowed_root")
        if isinstance(path, str) and path in seen_paths:
            violations.append(f"file_{index}:path_must_be_unique")
        if isinstance(path, str):
            seen_paths.add(path)
        if item.get("owner") != "root" or item.get("group") != "root":
            violations.append(f"file_{index}:ownership_must_be_root_root")
        if item.get("mode") not in _ALLOWED_MODES:
            violations.append(f"file_{index}:mode_must_be_restrictive")
        digest = item.get("sha256")
        if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
            violations.append(f"file_{index}:sha256_is_invalid")
        if not isinstance(item.get("managed_by_role"), str) or not item["managed_by_role"].strip():
            violations.append(f"file_{index}:managed_by_role_is_required")
    return tuple(violations)


def sensitive_file_contract_is_safe(files: list[dict[str, object]], **policy: object) -> bool:
    return not sensitive_file_contract_violations(files, **policy)

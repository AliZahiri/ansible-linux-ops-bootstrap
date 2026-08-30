from __future__ import annotations

from datetime import datetime
import shlex


_FORBIDDEN_EXECUTABLES = frozenset({"/bin/bash", "/bin/sh", "/usr/bin/bash", "/usr/bin/env", "/usr/bin/python", "/usr/bin/python3"})
_FORBIDDEN_METACHARACTERS = frozenset("*?[];|&$><")


def sudo_command_scope_violations(grants: list[dict[str, object]], *, now: datetime, maximum_passwordless_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_passwordless_seconds, int) or isinstance(maximum_passwordless_seconds, bool) or maximum_passwordless_seconds < 1:
        raise ValueError("maximum_passwordless_seconds must be a positive integer")
    if not isinstance(grants, list) or not grants:
        return ("at_least_one_sudo_grant_is_required",)
    violations: list[str] = []
    seen_grants: set[str] = set()
    for index, grant in enumerate(grants):
        if not isinstance(grant, dict):
            violations.append(f"grant_{index}:must_be_an_object")
            continue
        grant_id = grant.get("grant_id")
        if not isinstance(grant_id, str) or not grant_id.strip():
            violations.append(f"grant_{index}:grant_id_is_required")
        elif grant_id in seen_grants:
            violations.append(f"grant_{index}:grant_id_must_be_unique")
        else:
            seen_grants.add(grant_id)
        for field in ("subject", "run_as"):
            if not isinstance(grant.get(field), str) or not grant[field].strip():
                violations.append(f"grant_{index}:{field}_is_required")
        commands = grant.get("commands")
        if not isinstance(commands, list) or not commands:
            violations.append(f"grant_{index}:commands_must_be_a_non_empty_list")
        else:
            for command_index, command in enumerate(commands):
                if not _command_is_scoped(command):
                    violations.append(f"grant_{index}:command_{command_index}_is_not_literal_and_scoped")
        passwordless = grant.get("passwordless")
        if not isinstance(passwordless, bool):
            violations.append(f"grant_{index}:passwordless_must_be_boolean")
        elif passwordless:
            if not isinstance(grant.get("approval_ticket"), str) or not grant["approval_ticket"].strip():
                violations.append(f"grant_{index}:passwordless_approval_ticket_is_required")
            expires_at = _timestamp(grant.get("expires_at"))
            if expires_at is None:
                violations.append(f"grant_{index}:passwordless_expiry_must_be_timezone_aware")
            else:
                remaining = (expires_at - now).total_seconds()
                if remaining <= 0 or remaining > maximum_passwordless_seconds:
                    violations.append(f"grant_{index}:passwordless_expiry_is_outside_policy")
    return tuple(violations)


def sudo_command_scope_is_safe(grants: list[dict[str, object]], **policy: object) -> bool:
    return not sudo_command_scope_violations(grants, **policy)


def _command_is_scoped(command: object) -> bool:
    if not isinstance(command, str) or not command.strip() or command.strip() == "ALL" or any(character in command for character in _FORBIDDEN_METACHARACTERS):
        return False
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    return bool(parts) and parts[0].startswith("/") and parts[0] not in _FORBIDDEN_EXECUTABLES


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

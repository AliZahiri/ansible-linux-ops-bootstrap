from __future__ import annotations

from pathlib import Path


def missing_role_entrypoints(root: Path, role_names: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        role_name
        for role_name in role_names
        if not (root / 'roles' / role_name / 'tasks' / 'main.yml').is_file()
    )


def role_contract_is_valid(root: Path, role_names: list[str] | tuple[str, ...]) -> bool:
    return not missing_role_entrypoints(root, role_names)

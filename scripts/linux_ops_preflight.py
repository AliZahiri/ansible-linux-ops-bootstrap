from __future__ import annotations

from pathlib import Path

from scripts.validate_inventory_contract import inventory_contract_violations
from scripts.validate_playbook_roles import missing_role_entrypoints
from scripts.validate_vault_references import plaintext_secret_variable_names


def linux_ops_preflight(*, root: Path, inventory_content: str, variables: dict[str, object], role_names: list[str] | tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    return {"inventory": inventory_contract_violations(inventory_content), "vault_references": plaintext_secret_variable_names(variables), "role_entrypoints": missing_role_entrypoints(root, role_names)}


def linux_ops_preflight_is_ready(**inputs: object) -> bool:
    return not any(linux_ops_preflight(**inputs).values())

from __future__ import annotations


_SECRET_SUFFIXES = ("_password", "_token", "_secret", "_private_key")


def plaintext_secret_variable_names(variables: dict[str, object], *, vault_prefix: str = "vault_") -> tuple[str, ...]:
    if not vault_prefix:
        raise ValueError("vault prefix is required")
    violations: list[str] = []
    for name, value in variables.items():
        normalized = name.lower().strip()
        if not normalized.endswith(_SECRET_SUFFIXES):
            continue
        expected_reference = "{{ " + vault_prefix + name + " }}"
        if value != expected_reference:
            violations.append(name)
    return tuple(sorted(violations))


def vault_references_are_valid(variables: dict[str, object], *, vault_prefix: str = "vault_") -> bool:
    return not plaintext_secret_variable_names(variables, vault_prefix=vault_prefix)

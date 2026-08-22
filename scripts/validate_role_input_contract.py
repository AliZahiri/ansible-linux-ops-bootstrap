from __future__ import annotations


def role_input_contract_violations(values: dict[str, object], required: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, dict):
        return ("role_values_must_be_an_object",)
    return tuple(f"{key}_is_required" for key in required if not isinstance(values.get(key), str) or not values[key].strip())


def role_input_contract_is_valid(values: dict[str, object], required: tuple[str, ...]) -> bool:
    return not role_input_contract_violations(values, required)

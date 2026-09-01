from __future__ import annotations


def ssh_authentication_violations(config: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if config.get("pubkey_authentication") is not True:
        violations.append("public_key_authentication_must_be_enabled")
    if config.get("password_authentication") is not False:
        violations.append("password_authentication_must_be_disabled")
    if config.get("kbd_interactive_authentication") is not False:
        violations.append("keyboard_interactive_authentication_must_be_disabled")
    if config.get("permit_root_login") != "no":
        violations.append("direct_root_login_must_be_disabled")
    methods = config.get("authentication_methods")
    if not isinstance(methods, str) or not methods.strip():
        violations.append("authentication_methods_is_required")
    else:
        alternatives = [item.strip().split(",") for item in methods.split()]
        if any(not alternative or any(method != "publickey" for method in alternative) for alternative in alternatives):
            violations.append("authentication_methods_must_use_public_key_only")
    return tuple(violations)


def ssh_authentication_is_hardened(config: dict[str, object]) -> bool:
    return not ssh_authentication_violations(config)

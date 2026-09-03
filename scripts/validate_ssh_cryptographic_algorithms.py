from __future__ import annotations


_DEFAULT_KEX = frozenset({"curve25519-sha256", "curve25519-sha256@libssh.org", "sntrup761x25519-sha512@openssh.com", "diffie-hellman-group16-sha512"})
_DEFAULT_CIPHERS = frozenset({"chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com", "aes128-gcm@openssh.com"})
_DEFAULT_MACS = frozenset({"hmac-sha2-512-etm@openssh.com", "hmac-sha2-256-etm@openssh.com"})


def ssh_cryptographic_algorithm_violations(config: dict[str, object], *, approved_kex: frozenset[str] = _DEFAULT_KEX, approved_ciphers: frozenset[str] = _DEFAULT_CIPHERS, approved_macs: frozenset[str] = _DEFAULT_MACS) -> tuple[str, ...]:
    for name, approved in (("approved_kex", approved_kex), ("approved_ciphers", approved_ciphers), ("approved_macs", approved_macs)):
        if not isinstance(approved, frozenset) or not approved or any(not isinstance(value, str) or not value.strip() for value in approved):
            raise ValueError(f"{name} must be a non-empty frozenset of strings")
    if not isinstance(config, dict):
        return ("ssh_crypto_config_must_be_an_object",)

    violations: list[str] = []
    for field, approved in (("kex_algorithms", approved_kex), ("ciphers", approved_ciphers), ("macs", approved_macs)):
        values = config.get(field)
        if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values):
            violations.append(f"{field}_must_be_a_non_empty_string_list")
            continue
        if len(set(values)) != len(values):
            violations.append(f"{field}_must_be_unique")
        for value in values:
            if value not in approved:
                violations.append(f"{field}:{value}:is_not_approved")
    return tuple(violations)


def ssh_cryptographic_algorithms_are_hardened(config: dict[str, object], **policy: object) -> bool:
    return not ssh_cryptographic_algorithm_violations(config, **policy)

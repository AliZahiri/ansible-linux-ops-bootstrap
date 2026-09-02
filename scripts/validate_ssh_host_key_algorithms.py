from __future__ import annotations


_APPROVED = frozenset({"ssh-ed25519", "ecdsa-sha2-nistp256", "rsa-sha2-256", "rsa-sha2-512"})
_DEPRECATED = frozenset({"ssh-dss", "ssh-rsa"})


def ssh_host_key_algorithm_violations(keys: list[dict[str, object]], *, minimum_rsa_bits: int = 3072) -> tuple[str, ...]:
    if not isinstance(minimum_rsa_bits, int) or isinstance(minimum_rsa_bits, bool) or minimum_rsa_bits < 2048:
        raise ValueError("minimum_rsa_bits must be an integer of at least 2048")
    if not isinstance(keys, list) or not keys:
        return ("at_least_one_host_key_algorithm_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    approved = 0
    for index, key in enumerate(keys):
        algorithm = key.get("algorithm") if isinstance(key, dict) else None
        if not isinstance(algorithm, str) or not algorithm.strip():
            violations.append(f"key_{index}:algorithm_is_required")
            continue
        if algorithm in seen:
            violations.append(f"key_{index}:algorithm_must_be_unique")
        seen.add(algorithm)
        if algorithm in _DEPRECATED:
            violations.append(f"key_{index}:deprecated_algorithm_is_forbidden")
        elif algorithm not in _APPROVED:
            violations.append(f"key_{index}:algorithm_is_not_approved")
        else:
            approved += 1
        if algorithm.startswith("rsa-"):
            bits = key.get("bits")
            if not isinstance(bits, int) or isinstance(bits, bool) or bits < minimum_rsa_bits:
                violations.append(f"key_{index}:rsa_key_size_is_below_minimum")
    if approved == 0:
        violations.append("at_least_one_approved_host_key_algorithm_is_required")
    return tuple(violations)


def ssh_host_key_algorithms_are_hardened(keys: list[dict[str, object]], **policy: object) -> bool:
    return not ssh_host_key_algorithm_violations(keys, **policy)

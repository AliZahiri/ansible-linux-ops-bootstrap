from __future__ import annotations

import ipaddress


def ssh_authorized_key_source_address_violations(entries: object) -> tuple[str, ...]:
    if not isinstance(entries, list) or not entries: return ('authorized_key_entries_must_be_a_non_empty_list',)
    violations: list[str] = []
    for position, entry in enumerate(entries):
        prefix=f'entry_{position}'
        if not isinstance(entry, dict): violations.append(f'{prefix}:entry_must_be_an_object'); continue
        ranges=entry.get('source_addresses')
        if not isinstance(ranges, list) or not ranges: violations.append(f'{prefix}:source_addresses_must_be_a_non_empty_list'); continue
        parsed=[]
        for address in ranges:
            try: network=ipaddress.ip_network(address, strict=True) if isinstance(address, str) else None
            except ValueError: network=None
            if network is None or network.prefixlen == 0: violations.append(f'{prefix}:source_address_must_be_a_bounded_cidr')
            else: parsed.append(str(network))
        if len(parsed) != len(set(parsed)): violations.append(f'{prefix}:source_addresses_must_be_unique')
    return tuple(violations)

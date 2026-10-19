from __future__ import annotations


def ssh_authorized_key_restriction_violations(entries: object) -> tuple[str, ...]:
    if not isinstance(entries, list) or not entries: return ('authorized_key_entries_must_be_a_non_empty_list',)
    violations: list[str] = []
    for position, entry in enumerate(entries):
        prefix = f'entry_{position}'
        if not isinstance(entry, dict): violations.append(f'{prefix}:entry_must_be_an_object'); continue
        if entry.get('allow_agent_forwarding') is not False: violations.append(f'{prefix}:agent_forwarding_must_be_disabled')
        if entry.get('allow_port_forwarding') is not False: violations.append(f'{prefix}:port_forwarding_must_be_disabled')
        interactive = entry.get('interactive_access')
        if not isinstance(interactive, bool): violations.append(f'{prefix}:interactive_access_must_be_explicit')
        elif not interactive:
            command = entry.get('forced_command')
            if not isinstance(command, str) or not command.strip(): violations.append(f'{prefix}:non_interactive_key_requires_forced_command')
            if entry.get('allow_pty') is not False: violations.append(f'{prefix}:non_interactive_key_must_disable_pty')
    return tuple(violations)

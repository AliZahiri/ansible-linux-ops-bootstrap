from __future__ import annotations

from datetime import datetime
from ipaddress import ip_address


def listening_socket_exposure_violations(
    evidence: object,
    *,
    allowed_public_ports: set[int],
) -> tuple[str, ...]:
    """Validate timestamped listener evidence against a public-port allowlist."""
    if any(not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535 for port in allowed_public_ports):
        raise ValueError("allowed_public_ports must contain valid integer ports")
    if not isinstance(evidence, dict):
        return ("evidence_must_be_an_object",)

    violations: list[str] = []
    sockets = evidence.get("sockets")
    if not isinstance(sockets, list) or not sockets:
        violations.append("sockets_must_be_a_non_empty_list")
        sockets = []
    seen: set[tuple[str, str, int]] = set()
    for index, socket in enumerate(sockets):
        if not isinstance(socket, dict):
            violations.append(f"socket_{index}:must_be_an_object")
            continue
        protocol = socket.get("protocol")
        if protocol not in {"tcp", "udp"}:
            violations.append(f"socket_{index}:protocol_must_be_tcp_or_udp")

        raw_address = socket.get("address")
        try:
            address = ip_address(raw_address) if isinstance(raw_address, str) else None
        except ValueError:
            address = None
        if address is None:
            violations.append(f"socket_{index}:address_must_be_an_ip_address")

        port = socket.get("port")
        valid_port = isinstance(port, int) and not isinstance(port, bool) and 1 <= port <= 65535
        if not valid_port:
            violations.append(f"socket_{index}:port_must_be_between_1_and_65535")
        if not isinstance(socket.get("process"), str) or not socket["process"].strip():
            violations.append(f"socket_{index}:process_is_required")

        if address is not None and valid_port:
            identity = (str(protocol), address.compressed, port)
            if identity in seen:
                violations.append(f"socket_{index}:listener_must_be_unique")
            else:
                seen.add(identity)
            if not address.is_loopback and port not in allowed_public_ports:
                violations.append(f"socket_{index}:public_port_{port}_is_not_allowed")

    if _timestamp(evidence.get("observed_at")) is None:
        violations.append("observed_at_must_be_timezone_aware")
    return tuple(violations)


def listening_socket_exposure_is_safe(evidence: object, *, allowed_public_ports: set[int]) -> bool:
    return not listening_socket_exposure_violations(evidence, allowed_public_ports=allowed_public_ports)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def handler_notification_violations(*, notifications: list[object] | tuple[object, ...], handlers: list[object] | tuple[object, ...]) -> tuple[str, ...]:
    violations: list[str] = []
    normalized_handlers = [name.strip() if isinstance(name, str) else "" for name in handlers]
    normalized_notifications = [name.strip() if isinstance(name, str) else "" for name in notifications]
    if any(not isinstance(name, str) for name in handlers):
        violations.append("handler_names_must_be_strings")
    if any(not isinstance(name, str) for name in notifications):
        violations.append("notification_names_must_be_strings")
    if any(not name for name in normalized_handlers):
        violations.append("blank_handler_name_is_forbidden")
    if any(not name for name in normalized_notifications):
        violations.append("blank_notification_name_is_forbidden")
    seen: set[str] = set()
    for name in normalized_handlers:
        if name and name in seen:
            violations.append(f"duplicate_handler_definition:{name}")
        seen.add(name)
    defined = {name for name in normalized_handlers if name}
    for name in sorted({name for name in normalized_notifications if name} - defined):
        violations.append(f"undefined_handler_notification:{name}")
    return tuple(violations)


def handler_notifications_are_valid(*, notifications: list[object] | tuple[object, ...], handlers: list[object] | tuple[object, ...]) -> bool:
    return not handler_notification_violations(notifications=notifications, handlers=handlers)


def handler_notification_report(
    *,
    notifications: list[object] | tuple[object, ...],
    handlers: list[object] | tuple[object, ...],
) -> dict[str, object]:
    violations = handler_notification_violations(notifications=notifications, handlers=handlers)
    return {
        "valid": not violations,
        "notification_count": len(notifications),
        "handler_count": len(handlers),
        "violations": list(violations),
    }


def load_contract(path: Path) -> tuple[list[object], list[object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("handler contract input must be a JSON object")
    notifications = payload.get("notifications")
    handlers = payload.get("handlers")
    if not isinstance(notifications, list):
        raise ValueError("notifications must be a JSON array")
    if not isinstance(handlers, list):
        raise ValueError("handlers must be a JSON array")
    return notifications, handlers


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Ansible handler notifications from a parsed contract.")
    parser.add_argument("input", type=Path, help="JSON object containing notifications and handler names.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        notifications, handlers = load_contract(args.input)
        report = handler_notification_report(notifications=notifications, handlers=handlers)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

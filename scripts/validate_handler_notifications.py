from __future__ import annotations


def handler_notification_violations(*, notifications: list[str] | tuple[str, ...], handlers: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    violations: list[str] = []
    normalized_handlers = [str(name).strip() for name in handlers]
    normalized_notifications = [str(name).strip() for name in notifications]
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


def handler_notifications_are_valid(*, notifications: list[str] | tuple[str, ...], handlers: list[str] | tuple[str, ...]) -> bool:
    return not handler_notification_violations(notifications=notifications, handlers=handlers)

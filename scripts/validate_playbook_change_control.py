from __future__ import annotations


_RISKY_MODULES = frozenset({"ansible.builtin.command", "ansible.builtin.shell", "ansible.builtin.reboot"})


def playbook_change_control_violations(tasks: list[object]) -> tuple[str, ...]:
    if not isinstance(tasks, list) or not tasks:
        return ("at_least_one_task_is_required",)
    violations: list[str] = []
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            violations.append(f"task_{index}:must_be_an_object")
            continue
        name = task.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"task_{index}:name_is_required")
        tags = task.get("tags")
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            violations.append(f"task_{index}:explicit_tags_are_required")
        module = task.get("module")
        if module in _RISKY_MODULES:
            for field in ("change_ticket", "rollback_plan"):
                if not isinstance(task.get(field), str) or not task[field].strip():
                    violations.append(f"task_{index}:{field}_is_required_for_risky_module")
    return tuple(violations)


def playbook_change_control_is_valid(tasks: list[object]) -> bool:
    return not playbook_change_control_violations(tasks)

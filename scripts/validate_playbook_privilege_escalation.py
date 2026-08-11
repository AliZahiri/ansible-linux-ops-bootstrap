from __future__ import annotations


def playbook_privilege_escalation_violations(tasks: list[dict[str, object]]) -> tuple[str, ...]:
    if not tasks:
        return ("at_least_one_task_is_required",)
    violations: list[str] = []
    seen_names: set[str] = set()
    for index, task in enumerate(tasks):
        name = task.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"task_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"task_{index}:name_must_be_unique")
        seen_names.add(name)
        become = task.get("become")
        if not isinstance(become, bool):
            violations.append(f"task_{index}:become_must_be_explicit_boolean")
        elif become is True:
            if not isinstance(task.get("escalation_reason"), str) or not task["escalation_reason"].strip():
                violations.append(f"task_{index}:privileged_task_requires_reason")
        elif not isinstance(task.get("run_as"), str) or not task["run_as"].strip() or task["run_as"] == "root":
            violations.append(f"task_{index}:non_privileged_task_requires_non_root_user")
    return tuple(violations)


def playbook_privilege_escalation_is_safe(tasks: list[dict[str, object]]) -> bool:
    return not playbook_privilege_escalation_violations(tasks)

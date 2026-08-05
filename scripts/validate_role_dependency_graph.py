from __future__ import annotations


def role_dependency_graph_violations(roles: list[dict[str, object]]) -> tuple[str, ...]:
    if not roles:
        return ("at_least_one_role_is_required",)

    violations: list[str] = []
    graph: dict[str, set[str]] = {}
    for index, role in enumerate(roles):
        name = str(role.get("name", "")).strip()
        if not name:
            violations.append(f"role_{index}:name_is_required")
            continue
        if name in graph:
            violations.append(f"role_{index}:name_must_be_unique")
            continue
        dependencies = role.get("dependencies", [])
        if not isinstance(dependencies, list):
            violations.append(f"role:{name}:dependencies_must_be_a_list")
            dependencies = []
        graph[name] = {dependency.strip() for dependency in dependencies if isinstance(dependency, str) and dependency.strip()}
        if len(graph[name]) != len(dependencies):
            violations.append(f"role:{name}:dependencies_must_contain_non_empty_unique_names")

    for name, dependencies in graph.items():
        for dependency in dependencies:
            if dependency == name:
                violations.append(f"role:{name}:cannot_depend_on_itself")
            elif dependency not in graph:
                violations.append(f"role:{name}:dependency:{dependency}:is_not_declared")

    visiting: set[str] = set()
    visited: set[str] = set()

    def has_cycle(name: str) -> bool:
        if name in visiting:
            return True
        if name in visited:
            return False
        visiting.add(name)
        cyclic = any(has_cycle(dependency) for dependency in graph[name] if dependency in graph)
        visiting.remove(name)
        visited.add(name)
        return cyclic

    if any(has_cycle(name) for name in graph):
        violations.append("role_dependency_cycle_detected")
    return tuple(violations)


def role_dependency_graph_is_valid(roles: list[dict[str, object]]) -> bool:
    return not role_dependency_graph_violations(roles)

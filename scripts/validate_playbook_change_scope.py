from __future__ import annotations


def playbook_change_scope_violations(evidence: dict[str, object], *, maximum_hosts: int = 100) -> tuple[str, ...]:
    if not isinstance(maximum_hosts, int) or isinstance(maximum_hosts, bool) or maximum_hosts <= 0:
        raise ValueError("maximum hosts must be a positive integer")
    violations: list[str] = []
    inventory = evidence.get("inventory")
    if not isinstance(inventory, str) or not inventory.strip() or inventory == "production.ini":
        violations.append("inventory_must_be_an_explicit_non_default_name")
    host_count = evidence.get("host_count")
    if not isinstance(host_count, int) or isinstance(host_count, bool) or not 1 <= host_count <= maximum_hosts:
        violations.append("host_count_must_be_within_review_limit")
    tags = evidence.get("tags")
    if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        violations.append("tags_must_be_a_non_empty_string_list")
    if evidence.get("has_destructive_changes") is True and evidence.get("operator_acknowledged") is not True:
        violations.append("destructive_changes_require_operator_acknowledgement")
    return tuple(violations)


def playbook_change_scope_is_safe(evidence: dict[str, object], **limits: object) -> bool:
    return not playbook_change_scope_violations(evidence, **limits)

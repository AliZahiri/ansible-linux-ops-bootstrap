# Add Ansible role dependency graph gate

<!-- daily-pr-task: ansible-role-dependency-graph-gate -->

Ansible role ordering becomes hard to reason about when dependencies are implicit, missing, or cyclic. This offline gate validates supplied role metadata: unique role names, declared dependency targets, no self-dependencies, and an acyclic dependency graph. It checks metadata only and does not run a playbook or connect to inventory hosts.

## Portfolio Value

Makes role composition predictable before a bootstrap run by exposing missing, self-referential, duplicate, and cyclic dependencies in reviewable metadata.

## Validation

Run `python3 -m unittest discover -s tests` and confirm an acyclic declared graph passes while empty metadata, duplicate roles, self or unknown dependencies, and cycles fail.

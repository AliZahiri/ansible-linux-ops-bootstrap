# Add Ansible playbook privilege-escalation gate

<!-- daily-pr-task: playbook-privilege-escalation-gate -->

Privilege escalation in automation should be narrowly justified and reviewable. This offline gate validates task metadata: unique task names, explicit become use, an approved escalation reason for privileged tasks, and a declared non-root user for tasks that do not need root. It evaluates planning evidence without running a playbook.

## Portfolio Value

Shows disciplined least-privilege thinking in Ansible workflows instead of treating become access as an invisible default.

## Validation

Run `python3 -m unittest discover -s tests` and confirm explicitly justified privileged and non-root tasks pass while empty input, duplicate or unnamed tasks, implicit become, unjustified escalation, and root non-privileged execution fail.

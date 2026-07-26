# Add Ansible handler notification contract

<!-- daily-pr-task: ansible-handler-notification-contract -->

Ansible accepts notification names as strings, so a renamed or misspelled handler can silently break the intended restart or reload path until runtime. This dependency-free validator operates on already parsed task notifications and handler names, rejects blank or duplicate handler definitions, and reports every undefined notification using exact Ansible case-sensitive matching.

## Portfolio Value

Adds a deterministic Ansible wiring check that catches broken reload/restart notifications before playbook execution without requiring inventory access.

## Validation

Run `python3 -m unittest discover -s tests` and confirm defined notifications pass while blank names, duplicate handler definitions, undefined notifications, and case mismatches fail.

# Add SSH authorized-key restriction gate

<!-- daily-pr-task: ssh-authorized-key-restriction-gate -->

A time-bounded SSH key can still provide broader access than its task requires. This offline gate validates non-secret key-option metadata for restricted automation accounts: agent and port forwarding must be disabled, PTY allocation must be explicit, and a forced command must be present when interactive access is forbidden. It does not store a public key or alter a host.

## Portfolio Value

Extends key lifecycle evidence with enforceable least-privilege metadata, reducing the blast radius of automation SSH access.

## Validation

Run python3 -m unittest discover -s tests and confirm restricted automation-key metadata passes while forwarding, missing forced commands, and implicit access modes fail.

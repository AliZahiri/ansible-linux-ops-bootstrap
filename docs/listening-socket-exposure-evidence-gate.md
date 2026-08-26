# Listening socket exposure evidence gate

Firewall and service configuration intent should be checked against the listeners actually observed after a playbook run. The offline validator in `scripts/validate_listening_socket_exposure.py` compares timestamped socket metadata with an explicit public-port allowlist.

Each observation needs a TCP or UDP protocol, an IP address, a valid port, and a process name. Duplicate listeners fail, as does any non-loopback listener whose port is not allowed. The validator consumes evidence only; it does not run privileged probes, connect to a host, or require inventory credentials in CI.

Run the focused tests with:

```bash
python3 -m unittest tests.test_validate_listening_socket_exposure
```

Generate evidence from a trusted post-deployment collection step, review the allowlist as code, and pair this gate with firewall, SSH, exporter, and service health controls.

# Add Linux core dump policy evidence gate

<!-- daily-pr-task: linux-core-dump-policy-evidence-gate -->

Core dumps can persist credentials and application data even when package configuration appears hardened. This offline gate validates fresh effective-state evidence for systemd-coredump storage, process resource limits, suid dumpability, and core-pattern handling without collecting dump contents or host secrets.

## Portfolio Value

Adds verifiable effective-state hardening for a common secret-exposure path that configuration-only Linux baselines can miss.

## Validation

Run python3 -m unittest discover -s tests and confirm fresh evidence with discarded dumps and zero limits passes while persistent storage, nonzero limits, suid dumping, unsafe patterns, stale timestamps, and invalid policy fail.

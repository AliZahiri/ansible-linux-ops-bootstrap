# Add filesystem capacity and inode evidence gate

<!-- daily-pr-task: filesystem-capacity-inode-evidence-gate -->

Byte capacity alone can look healthy while inode exhaustion prevents logs, backups, or package operations from creating files. This deterministic preflight validates unique absolute mount points, writable state, and both byte and inode utilization against configurable ceilings. It consumes inventory evidence without changing a host.

## Portfolio Value

Extends Linux preflight checks beyond free bytes by detecting inode exhaustion and read-only mounts before they break logging, backups, package updates, or service recovery.

## Validation

Run `python3 -m unittest discover -s tests` and confirm healthy writable mounts pass while empty input, relative or duplicate mounts, read-only state, invalid or excessive byte/inode utilization, and invalid thresholds fail.

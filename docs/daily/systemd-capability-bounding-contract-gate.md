# Add systemd capability bounding contract gate

<!-- daily-pr-task: systemd-capability-bounding-contract-gate -->

A non-root service can still receive broad Linux capabilities. This offline contract requires explicit capability bounds, rejects ambient capabilities, and blocks high-risk capabilities such as CAP_SYS_ADMIN before a unit definition is promoted. It validates declared metadata only and does not change a host.

## Portfolio Value

Extends systemd hardening from runtime identity to explicit Linux privilege boundaries that are reviewable before rollout.

## Validation

Run python3 -m unittest discover -s tests and confirm bounded, non-ambient capability sets pass while forbidden, duplicate, or ambient privileges fail.

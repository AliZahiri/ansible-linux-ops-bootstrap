# Add time synchronization health evidence gate

<!-- daily-pr-task: time-sync-health-evidence-gate -->

Reliable audit trails, TLS validation, and distributed incident timelines depend on bounded clock error, not merely an installed NTP package. This offline gate validates synchronization state, usable source count, stratum, leap status, and finite measured offset against an operator-defined ceiling. It evaluates supplied evidence and never contacts hosts.

## Portfolio Value

Adds deterministic host clock evidence needed for trustworthy logs, certificate validation, scheduled automation, and incident reconstruction without coupling CI to live inventory.

## Validation

Run `python3 -m unittest discover -s tests` and confirm synchronized bounded clocks pass while missing sources, invalid strata, non-finite or excessive offsets, abnormal leap state, and invalid policy values fail.

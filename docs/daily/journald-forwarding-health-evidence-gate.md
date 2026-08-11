# Add journald forwarding health evidence gate

<!-- daily-pr-task: journald-forwarding-health-evidence-gate -->

Persistent local journald retention is not enough when host evidence must reach a central operations system. This offline gate validates forwarding observations: unique host identities, enabled forwarding, a recent successful delivery timestamp, and non-negative backlog count. It checks supplied telemetry only and never connects to a log collector.

## Portfolio Value

Extends Linux logging from local retention to verifiable centralized-delivery health, which is essential for incident visibility.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fresh enabled delivery passes while empty input, duplicate hosts, disabled forwarding, stale or invalid timestamps, negative backlog, and invalid policy values fail.

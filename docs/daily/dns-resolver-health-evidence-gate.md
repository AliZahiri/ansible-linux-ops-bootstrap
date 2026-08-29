# Add DNS resolver health evidence gate

<!-- daily-pr-task: dns-resolver-health-evidence-gate -->

Static resolver configuration does not prove that a host can resolve service names. This offline gate validates exported per-host DNS evidence: unique host identities, multiple unique nameservers, a recent successful lookup, and bounded resolution latency. It consumes non-sensitive summaries only and makes no network calls in CI.

## Portfolio Value

Connects Linux resolver configuration to fresh runtime evidence so bootstrap validation can detect single-resolver dependency, failed lookups, and degraded DNS before application rollout.

## Validation

Run python3 -m unittest discover -s tests and confirm empty evidence, duplicate hosts or nameservers, insufficient resolver coverage, stale or failed lookups, latency breaches, malformed measurements, and invalid policy fail.

# Add Docker daemon runtime evidence gate

<!-- daily-pr-task: docker-daemon-runtime-evidence-gate -->

Docker hardening templates need fresh evidence from the running daemon. This offline gate validates supplied daemon observations: a rootless or user-namespace boundary, live-restore enabled, a supported structured log driver, bounded log rotation, and a recent timezone-aware observation. It does not query Docker.

## Portfolio Value

Turns Docker daemon hardening from template intent into fresh operational evidence without exposing daemon configuration secrets.

## Validation

Run `python3 -m unittest discover -s tests` and confirm fresh hardened daemon evidence passes while absent resilience controls, unsafe logging, stale observations, and invalid policy values fail.

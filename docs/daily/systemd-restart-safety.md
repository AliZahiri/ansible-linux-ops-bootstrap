# Add systemd restart safety drop-in

<!-- daily-pr-task: systemd-restart-safety -->

Systemd services should restart predictably without hiding crash loops. A small restart-safety drop-in can bound restart bursts and make failures visible to operators.

Recommended controls:

- restart on failure only
- short but bounded restart delay
- start limit interval
- start limit burst
- clear tests for generated unit policy

## Portfolio Value

Adds concrete operational safety around Linux service reliability and crash-loop handling.

## Validation

Run `python3 -m unittest discover -s tests` and confirm restart limits are present in the template.

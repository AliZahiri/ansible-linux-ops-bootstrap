# Add Ansible collection version-lock gate

<!-- daily-pr-task: ansible-collection-version-lock-gate -->

Automation should not silently drift when required Ansible collections resolve to newer versions. This offline gate validates declared collection locks: names are unique, versions use an exact semantic-version pin, and each declaration includes a trusted source identifier. It checks metadata only and does not download collections or access production hosts.

## Portfolio Value

Makes external Ansible dependencies reviewable and reproducible so a bootstrap run does not inherit unreviewed collection behavior.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unique exact HTTPS-backed collection locks pass while empty, duplicate, malformed, floating, and non-HTTPS declarations fail.

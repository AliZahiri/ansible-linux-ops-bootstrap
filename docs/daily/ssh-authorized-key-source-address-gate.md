# Add SSH authorized-key source-address gate

<!-- daily-pr-task: ssh-authorized-key-source-address-gate -->

A restricted SSH key should also be constrained to its expected network sources when the deployment model allows it. This offline gate validates non-secret authorized-key metadata: each account/fingerprint assignment has a non-empty, unique list of CIDR source ranges and does not use an unrestricted address range. It does not read keys or change firewall rules.

## Portfolio Value

Adds a reviewable network-origin restriction to SSH key governance, reducing exposure even when a key remains valid and time-bounded.

## Validation

Run python3 -m unittest discover -s tests and confirm unique bounded IPv4/IPv6 CIDRs pass while unrestricted, invalid, and duplicate ranges fail.

# Add SSH authorized-key expiry gate

<!-- daily-pr-task: ssh-authorized-key-expiry-gate -->

An approved public key should not become permanent access merely because it was once reviewed. This offline gate validates non-secret authorized-key lifecycle metadata: a future expiry timestamp, a bounded maximum lifetime, and a unique fingerprint per account. It does not store key material or change host configuration.

## Portfolio Value

Adds time-bounded access control evidence for SSH keys, complementing provenance checks without recording credential material.

## Validation

Run python3 -m unittest discover -s tests and confirm future, short-lived unique key assignments pass while expired, overlong, and duplicate assignments fail.

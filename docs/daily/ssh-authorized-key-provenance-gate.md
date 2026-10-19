# Add SSH authorized-key provenance gate

<!-- daily-pr-task: ssh-authorized-key-provenance-gate -->

Authorized-key files are security-sensitive access paths, but storing public keys in validation evidence is unnecessary. This offline gate validates only non-secret key metadata: a non-root account, an OpenSSH SHA-256 fingerprint, a change reference, and a recent review timestamp. It rejects duplicate account/fingerprint assignments and does not read private keys or modify hosts.

## Portfolio Value

Strengthens SSH access governance with reviewable, non-secret provenance evidence for authorized keys while keeping credential material out of the repository.

## Validation

Run python3 -m unittest discover -s tests and confirm recent non-root key metadata passes while stale, root, duplicate, or untraceable assignments fail.

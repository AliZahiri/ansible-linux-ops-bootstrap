# Add SSH host key algorithm contract gate

<!-- daily-pr-task: ssh-host-key-algorithm-contract-gate -->

Host-key presence does not prove that sshd offers only approved cryptographic algorithms. This offline gate validates unique effective host-key algorithms, rejects deprecated DSA and SHA-1 RSA signatures, requires at least one modern algorithm, and enforces a minimum RSA key size without reading private keys.

## Portfolio Value

Adds effective cryptographic-policy validation to SSH hardening so a valid daemon configuration cannot silently retain deprecated host-key signatures.

## Validation

Run python3 -m unittest discover -s tests and confirm unique approved Ed25519, ECDSA, or SHA-2 RSA algorithms pass while deprecated, unknown, duplicate, weak RSA, empty evidence, and invalid policy fail.

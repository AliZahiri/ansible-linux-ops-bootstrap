# Add SSH cryptographic algorithm contract gate

<!-- daily-pr-task: ssh-cryptographic-algorithm-contract-gate -->

Host keys and authentication settings do not describe the complete SSH cryptographic surface. This offline gate validates effective key-exchange, cipher, and MAC allowlists against a conservative modern baseline. The baseline is intentionally configurable for compatibility planning and validates declared effective configuration without reading keys or opening network connections.

## Portfolio Value

Completes SSH hardening evidence with the negotiated-algorithm surface, preventing key-only reviews from overlooking legacy encryption or integrity primitives.

## Validation

Run python3 -m unittest discover -s tests and confirm only unique approved key-exchange, cipher, and MAC lists pass while legacy, duplicate, missing, malformed, and invalid-policy cases fail.

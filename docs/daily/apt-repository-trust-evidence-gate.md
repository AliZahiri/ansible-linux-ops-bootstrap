# Add APT repository trust evidence gate

<!-- daily-pr-task: apt-repository-trust-evidence-gate -->

Linux bootstrap automation inherits the trust of every configured package repository. This offline gate validates supplied APT repository verification evidence: unique repository identities, a dedicated /etc/apt/keyrings signing-key path, a valid OpenPGP fingerprint, successful signature verification, and fresh timezone-aware observations. It does not run apt, fetch keys, or change a host.

## Portfolio Value

Extends Linux bootstrap hardening to package-source provenance so repository signing evidence is explicit, fresh, and reviewable before automation trusts it.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unique verified fresh repositories pass while insecure key paths, malformed fingerprints, failed signatures, stale or naive timestamps, duplicate names, and invalid policy values fail.

# Backup key rotation gate

Backup evidence should include an active key identifier and a recent timezone-aware rotation timestamp. This offline check keeps encryption-key rotation reviewable without storing keys or vault passwords in the repository.

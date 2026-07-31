import unittest
from datetime import datetime, timezone

from scripts.validate_backup_encryption_evidence import backup_encryption_evidence_is_acceptable, backup_encryption_evidence_violations


NOW = datetime(2026, 7, 31, 10, 0, tzinfo=timezone.utc)


class BackupEncryptionEvidenceGateTests(unittest.TestCase):
    def test_fresh_encrypted_verified_backup_passes(self):
        evidence = {"encrypted": True, "algorithm": "AES-256-GCM", "key_reference": "kms://backup/production-v3", "checksum_verified": True, "plaintext_removed": True, "observed_at": "2026-07-31T09:30:00Z"}
        self.assertTrue(backup_encryption_evidence_is_acceptable(evidence, now=NOW))

    def test_unencrypted_unverified_plaintext_evidence_fails(self):
        evidence = {"encrypted": False, "algorithm": "AES-CBC", "key_reference": "literal-secret", "checksum_verified": False, "plaintext_removed": False, "observed_at": "2026-07-31T07:00:00Z"}
        violations = backup_encryption_evidence_violations(evidence, now=NOW)
        self.assertIn("backup_must_be_encrypted", violations)
        self.assertIn("backup_encryption_algorithm_is_not_approved", violations)
        self.assertIn("external_key_reference_is_invalid", violations)
        self.assertIn("encrypted_backup_checksum_must_be_verified", violations)
        self.assertIn("plaintext_backup_material_must_be_removed", violations)
        self.assertIn("encryption_evidence_is_stale", violations)

    def test_naive_timestamp_and_invalid_policy_fail(self):
        evidence = {"encrypted": True, "algorithm": "AES-256-GCM", "key_reference": "vault://backup/key", "checksum_verified": True, "plaintext_removed": True, "observed_at": "2026-07-31T10:00:00"}
        self.assertIn("observed_at_must_be_timezone_aware", backup_encryption_evidence_violations(evidence, now=NOW))
        with self.assertRaises(ValueError):
            backup_encryption_evidence_violations({}, now=NOW, maximum_age_seconds=0)


if __name__ == "__main__":
    unittest.main()

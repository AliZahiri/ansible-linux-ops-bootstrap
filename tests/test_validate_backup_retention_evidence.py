import unittest

from scripts.validate_backup_retention_evidence import backup_retention_evidence_is_valid, backup_retention_evidence_violations


class BackupRetentionEvidenceGateTests(unittest.TestCase):
    def test_verified_timezone_aware_retention_passes(self):
        evidence = {"tiers": {"daily": "2026-08-16T00:00:00Z", "weekly": "2026-08-10T00:00:00Z", "monthly": "2026-07-01T00:00:00Z"}, "retention_verified": True}
        self.assertTrue(backup_retention_evidence_is_valid(evidence))

    def test_missing_tier_naive_timestamp_and_failed_verification_fail(self):
        violations = backup_retention_evidence_violations({"tiers": {"daily": "2026-08-16T00:00:00", "weekly": "2026-08-10T00:00:00Z"}, "retention_verified": False})
        self.assertEqual(violations, ("required_retention_tiers_are_missing",))


if __name__ == "__main__":
    unittest.main()

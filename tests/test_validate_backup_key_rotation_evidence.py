import unittest
from datetime import datetime, timezone

from scripts.validate_backup_key_rotation_evidence import backup_key_rotation_evidence_is_valid, backup_key_rotation_evidence_violations


NOW = datetime(2026, 8, 19, 6, 0, tzinfo=timezone.utc)


class BackupKeyRotationEvidenceTests(unittest.TestCase):
    def test_recent_verified_active_key_evidence_passes(self):
        evidence = {"key_id": "backup-key-2026-08", "backup_scope": "postgres", "active": True, "rotation_verified": True, "rotated_at": "2026-08-01T00:00:00Z", "expires_at": "2026-11-01T00:00:00Z"}
        self.assertTrue(backup_key_rotation_evidence_is_valid(evidence, now=NOW))

    def test_missing_inactive_stale_and_expired_evidence_fails(self):
        evidence = {"active": False, "rotation_verified": False, "rotated_at": "2026-01-01T00:00:00Z", "expires_at": "2026-08-01T00:00:00Z"}
        violations = backup_key_rotation_evidence_violations(evidence, now=NOW)
        self.assertIn("key_id_is_required", violations)
        self.assertIn("backup_scope_is_required", violations)
        self.assertIn("backup_key_must_be_active", violations)
        self.assertIn("rotation_verification_must_pass", violations)
        self.assertIn("key_rotation_is_not_fresh", violations)
        self.assertIn("backup_key_must_not_be_expired", violations)

    def test_invalid_policy_and_naive_clock_fail(self):
        with self.assertRaises(ValueError):
            backup_key_rotation_evidence_violations({}, now=NOW, maximum_age_days=0)
        with self.assertRaises(ValueError):
            backup_key_rotation_evidence_violations({}, now=datetime(2026, 8, 19, 6, 0))

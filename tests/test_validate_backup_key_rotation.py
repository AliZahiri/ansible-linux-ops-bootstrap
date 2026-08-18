import unittest
from datetime import datetime, timezone

from scripts.validate_backup_key_rotation import backup_key_rotation_is_current, backup_key_rotation_violations


class BackupKeyRotationTests(unittest.TestCase):
    def test_recent_active_key_passes(self):
        evidence = {"key_id": "backup-key-2", "active": True, "rotated_at": "2026-08-01T00:00:00Z"}
        self.assertTrue(backup_key_rotation_is_current(evidence, now=datetime(2026, 8, 18, tzinfo=timezone.utc)))

    def test_missing_inactive_and_stale_key_fails(self):
        violations = backup_key_rotation_violations({"active": False, "rotated_at": "2026-01-01T00:00:00Z"}, now=datetime(2026, 8, 18, tzinfo=timezone.utc))
        self.assertIn("key_id_is_required", violations)
        self.assertIn("backup_key_must_be_active", violations)
        self.assertIn("backup_key_rotation_is_stale", violations)


if __name__ == "__main__":
    unittest.main()

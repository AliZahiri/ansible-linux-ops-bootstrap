import unittest
from datetime import datetime, timezone

from scripts.validate_backup_restore_point_diversity import backup_restore_point_diversity_violations, backup_restore_points_are_diverse


NOW = datetime(2026, 8, 14, 6, 0, tzinfo=timezone.utc)


class BackupRestorePointDiversityGateTests(unittest.TestCase):
    def test_distinct_recent_restore_points_pass(self):
        points = [{"backup_id": f"backup-{day}", "sha256": chr(96 + day) * 64, "created_at": f"2026-08-{day:02d}T00:00:00Z"} for day in (11, 12, 13)]
        self.assertTrue(backup_restore_points_are_diverse(points, now=NOW))

    def test_sparse_duplicate_invalid_and_stale_points_fail(self):
        points = [{"backup_id": "backup", "sha256": "bad", "created_at": "2026-07-01T00:00:00Z"}, {"backup_id": "backup", "sha256": "a" * 64, "created_at": "2026-08-13T00:00:00Z"}]
        violations = backup_restore_point_diversity_violations(points, now=NOW)
        self.assertIn("minimum_restore_point_count_is_not_met", violations)
        self.assertIn("point_0:sha256_is_invalid", violations)
        self.assertIn("point_0:restore_point_is_not_within_age_budget", violations)
        self.assertIn("point_1:backup_id_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()

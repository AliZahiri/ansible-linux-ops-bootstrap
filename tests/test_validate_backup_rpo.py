import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_backup_rpo.py"
SPEC = importlib.util.spec_from_file_location("validate_backup_rpo", SCRIPT_PATH)
validate_backup_rpo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_backup_rpo)


class BackupRpoPolicyTests(unittest.TestCase):
    def test_recent_backup_meets_rpo(self):
        self.assertTrue(validate_backup_rpo.backup_meets_rpo(last_success_at="2026-07-21T10:00:00Z", observed_at="2026-07-21T10:30:00Z", max_age_seconds=3600))

    def test_stale_backup_is_reported(self):
        self.assertEqual(("backup_exceeds_recovery_point_objective",), validate_backup_rpo.backup_rpo_violations(last_success_at="2026-07-21T08:00:00Z", observed_at="2026-07-21T10:00:01Z", max_age_seconds=7200))

    def test_naive_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_backup_rpo.backup_meets_rpo(last_success_at="2026-07-21T10:00:00", observed_at="2026-07-21T10:30:00Z", max_age_seconds=3600)


if __name__ == "__main__":
    unittest.main()

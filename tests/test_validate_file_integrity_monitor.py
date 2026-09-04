import unittest
from datetime import datetime, timezone

from scripts.validate_file_integrity_monitor import file_integrity_monitor_is_verified, file_integrity_monitor_violations


NOW = datetime(2026, 9, 4, 6, 0, tzinfo=timezone.utc)


class FileIntegrityMonitorEvidenceTests(unittest.TestCase):
    def test_fresh_successful_unchanged_scan_passes(self):
        evidence = {"scheduler_active": True, "baseline_sha256": "sha256:" + "a" * 64, "scan_succeeded": True, "reviewed_critical_change_count": 0, "scan_completed_at": "2026-09-04T05:30:00Z"}
        self.assertTrue(file_integrity_monitor_is_verified(evidence, now=NOW))

    def test_inactive_failed_changed_and_stale_scan_fails(self):
        evidence = {"scheduler_active": False, "baseline_sha256": "bad", "scan_succeeded": False, "reviewed_critical_change_count": 2, "scan_completed_at": "2026-09-01T00:00:00Z"}
        violations = file_integrity_monitor_violations(evidence, now=NOW)
        self.assertIn("file_integrity_scheduler_must_be_active", violations)
        self.assertIn("file_integrity_baseline_sha256_must_be_a_digest", violations)
        self.assertIn("latest_file_integrity_scan_must_succeed", violations)
        self.assertIn("critical_file_changes_exceed_reviewed_budget", violations)
        self.assertIn("file_integrity_scan_is_invalid_stale_or_future_dated", violations)

    def test_invalid_shape_and_policy_fail(self):
        self.assertEqual(("file_integrity_evidence_must_be_an_object",), file_integrity_monitor_violations([], now=NOW))
        with self.assertRaises(ValueError):
            file_integrity_monitor_violations({}, now=NOW, maximum_scan_age_seconds=0)

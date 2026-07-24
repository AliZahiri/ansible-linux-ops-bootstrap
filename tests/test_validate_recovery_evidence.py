import unittest

from scripts.validate_recovery_evidence import recovery_evidence_is_ready, recovery_evidence_violations


def evidence():
    return {"backup_id": "backup-42", "backup_completed_at": "2026-07-23T09:00:00Z", "checksum_verified": True, "application_verification_passed": True, "started_at": "2026-07-23T09:10:00Z", "completed_at": "2026-07-23T09:20:00Z"}


class RecoveryEvidenceGateTests(unittest.TestCase):
    def test_recent_verified_restore_within_rto_passes(self):
        self.assertTrue(recovery_evidence_is_ready(evidence=evidence(), observed_at="2026-07-23T10:00:00Z", max_age_seconds=7200, max_duration_seconds=1800))

    def test_missing_identity_stale_backup_and_slow_restore_are_combined(self):
        invalid = evidence()
        invalid["backup_id"] = ""
        invalid["completed_at"] = "2026-07-23T11:00:00Z"
        violations = recovery_evidence_violations(evidence=invalid, observed_at="2026-07-23T12:00:00Z", max_age_seconds=3600, max_duration_seconds=1800)
        self.assertIn("backup_identifier_is_required", violations)
        self.assertIn("backup_exceeds_recovery_point_objective", violations)
        self.assertIn("restore_exceeds_recovery_time_objective", violations)


if __name__ == "__main__":
    unittest.main()

import unittest

from scripts.validate_backup_rpo_evidence import backup_rpo_evidence_is_valid, backup_rpo_evidence_violations


class BackupRpoEvidenceGateTests(unittest.TestCase):
    def test_recent_verified_backup_within_rpo_passes(self):
        evidence = {"rpo_minutes": 60, "observed_age_minutes": 45, "verified_at": "2026-08-20T08:00:00Z", "verification_passed": True}
        self.assertTrue(backup_rpo_evidence_is_valid(evidence))

    def test_invalid_overdue_and_unverified_evidence_fails(self):
        violations = backup_rpo_evidence_violations({"rpo_minutes": 0, "observed_age_minutes": -1, "verified_at": "2026-08-20T08:00:00", "verification_passed": False})
        self.assertEqual(violations, ("rpo_minutes_must_be_positive", "observed_age_minutes_must_be_non_negative", "verified_at_must_be_timezone_aware", "verification_must_pass"))

    def test_backup_age_above_rpo_is_reported(self):
        violations = backup_rpo_evidence_violations({"rpo_minutes": 60, "observed_age_minutes": 61, "verified_at": "2026-08-20T08:00:00Z", "verification_passed": True})
        self.assertEqual(violations, ("backup_age_exceeds_rpo",))

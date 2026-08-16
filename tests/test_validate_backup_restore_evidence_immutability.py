import unittest

from scripts.validate_backup_restore_evidence_immutability import restore_evidence_is_immutable, restore_evidence_immutability_violations


class BackupRestoreEvidenceImmutabilityGateTests(unittest.TestCase):
    def test_complete_immutable_evidence_passes(self):
        self.assertTrue(restore_evidence_is_immutable({"artifact_sha256": "c" * 64, "immutable_storage": True, "verified_at": "2026-08-16T12:00:00Z", "integrity_check_passed": True, "application_check_passed": True}))

    def test_incomplete_evidence_reports_all_controls(self):
        violations = restore_evidence_immutability_violations({"artifact_sha256": "bad", "immutable_storage": False, "verified_at": "2026-08-16T12:00:00", "integrity_check_passed": False, "application_check_passed": False})
        self.assertEqual(len(violations), 5)


if __name__ == "__main__":
    unittest.main()

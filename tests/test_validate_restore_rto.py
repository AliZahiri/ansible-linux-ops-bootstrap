import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_restore_rto.py"
SPEC = importlib.util.spec_from_file_location("validate_restore_rto", SCRIPT_PATH)
validate_restore_rto = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_restore_rto)


class RestoreRtoEvidenceTests(unittest.TestCase):
    def test_verified_restore_within_rto_passes(self):
        evidence = {"checksum_verified": True, "application_verification_passed": True, "started_at": "2026-07-21T10:00:00Z", "completed_at": "2026-07-21T10:20:00Z"}
        self.assertTrue(validate_restore_rto.restore_meets_rto(evidence, max_duration_seconds=1800))

    def test_slow_restore_is_reported(self):
        evidence = {"checksum_verified": True, "application_verification_passed": True, "started_at": "2026-07-21T10:00:00Z", "completed_at": "2026-07-21T11:00:01Z"}
        self.assertIn("restore_exceeds_recovery_time_objective", validate_restore_rto.restore_rto_violations(evidence, max_duration_seconds=3600))

    def test_integrity_and_application_evidence_are_required(self):
        violations = validate_restore_rto.restore_rto_violations({"started_at": "2026-07-21T10:00:00Z", "completed_at": "2026-07-21T10:10:00Z"}, max_duration_seconds=3600)
        self.assertIn("backup_checksum_not_verified", violations)
        self.assertIn("application_verification_not_passed", violations)


if __name__ == "__main__":
    unittest.main()

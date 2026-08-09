import unittest
from datetime import datetime, timezone

from scripts.validate_sudoers_evidence import sudoers_evidence_is_safe, sudoers_evidence_violations


NOW = datetime(2026, 8, 9, 5, 0, tzinfo=timezone.utc)
DIGEST = "a" * 64


class SudoersValidationEvidenceGateTests(unittest.TestCase):
    def test_root_owned_validated_fresh_fragment_passes(self):
        files = [{"path": "/etc/sudoers.d/ops", "owner": "root", "group": "root", "mode": "0440", "sha256": DIGEST, "visudo_check_passed": True, "verified_at": "2026-08-09T04:30:00Z"}]
        self.assertTrue(sudoers_evidence_is_safe(files, now=NOW))

    def test_unsafe_path_permissions_digest_and_stale_check_fail(self):
        files = [{"path": "/tmp/ops", "owner": "deploy", "group": "deploy", "mode": "0644", "sha256": "bad", "visudo_check_passed": False, "verified_at": "2026-08-01T00:00:00Z"}]
        violations = sudoers_evidence_violations(files, now=NOW)
        self.assertIn("file_0:path_must_be_a_sudoers_fragment", violations)
        self.assertIn("file_0:ownership_must_be_root_root", violations)
        self.assertIn("file_0:mode_must_be_0440", violations)
        self.assertIn("file_0:sha256_is_invalid", violations)
        self.assertIn("file_0:visudo_check_must_pass", violations)
        self.assertIn("file_0:verification_is_not_fresh", violations)

    def test_empty_input_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_sudoers_observation_is_required",), sudoers_evidence_violations([], now=NOW))
        with self.assertRaises(ValueError):
            sudoers_evidence_violations([], now=NOW, maximum_age_seconds=0)


if __name__ == "__main__":
    unittest.main()

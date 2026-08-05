import unittest
from datetime import datetime, timezone

from scripts.validate_apt_repository_trust import apt_repository_trust_is_current, apt_repository_trust_violations


NOW = datetime(2026, 8, 5, 10, 0, tzinfo=timezone.utc)
FINGERPRINT = "A" * 40


class AptRepositoryTrustEvidenceGateTests(unittest.TestCase):
    def test_unique_verified_fresh_repository_evidence_passes(self):
        repositories = [{"name": "docker", "signed_by": "/etc/apt/keyrings/docker.asc", "fingerprint": FINGERPRINT, "signature_verified": True, "verified_at": "2026-08-04T12:00:00Z"}]
        self.assertTrue(apt_repository_trust_is_current(repositories, now=NOW))

    def test_duplicate_untrusted_and_stale_repository_evidence_fails(self):
        repositories = [{"name": "docker", "signed_by": "/tmp/key.asc", "fingerprint": "bad", "signature_verified": False, "verified_at": "2026-06-01T00:00:00Z"}, {"name": "DOCKER", "signed_by": "/etc/apt/keyrings/docker.asc", "fingerprint": FINGERPRINT, "signature_verified": True, "verified_at": "2026-08-05T09:00:00"}]
        violations = apt_repository_trust_violations(repositories, now=NOW)
        self.assertIn("repository_0:signed_by_must_use_dedicated_keyring", violations)
        self.assertIn("repository_0:fingerprint_must_be_a_valid_openpgp_value", violations)
        self.assertIn("repository_0:signature_must_be_verified", violations)
        self.assertIn("repository_0:trust_evidence_is_not_fresh", violations)
        self.assertIn("repository_1:name_must_be_unique", violations)
        self.assertIn("repository_1:verified_at_must_be_timezone_aware", violations)

    def test_empty_evidence_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_repository_observation_is_required",), apt_repository_trust_violations([], now=NOW))
        with self.assertRaises(ValueError):
            apt_repository_trust_violations([], now=NOW, maximum_age_seconds=0)


if __name__ == "__main__":
    unittest.main()

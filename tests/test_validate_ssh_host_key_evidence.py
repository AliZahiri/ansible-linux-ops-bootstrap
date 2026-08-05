import unittest
from datetime import datetime, timezone

from scripts.validate_ssh_host_key_evidence import ssh_host_key_evidence_is_current, ssh_host_key_evidence_violations


NOW = datetime(2026, 8, 5, 9, 0, tzinfo=timezone.utc)
FINGERPRINT = "SHA256:" + "A" * 43


class SshHostKeyEvidenceGateTests(unittest.TestCase):
    def test_unique_strict_and_fresh_host_key_evidence_passes(self):
        hosts = [{"host": "api-1.example.com", "strict_host_key_checking": True, "fingerprint": FINGERPRINT, "verified_at": "2026-08-05T08:00:00Z"}, {"host": "db-1.example.com", "strict_host_key_checking": True, "fingerprint": FINGERPRINT, "verified_at": "2026-08-04T09:00:00Z"}]
        self.assertTrue(ssh_host_key_evidence_is_current(hosts, now=NOW))

    def test_duplicate_untrusted_malformed_and_stale_evidence_fails(self):
        hosts = [{"host": "api-1.example.com", "strict_host_key_checking": False, "fingerprint": "bad", "verified_at": "2026-06-01T00:00:00Z"}, {"host": "API-1.EXAMPLE.COM", "strict_host_key_checking": True, "fingerprint": FINGERPRINT, "verified_at": "2026-08-05T08:00:00"}]
        violations = ssh_host_key_evidence_violations(hosts, now=NOW)
        self.assertIn("host_0:strict_host_key_checking_must_be_enabled", violations)
        self.assertIn("host_0:fingerprint_must_be_an_openssh_sha256_value", violations)
        self.assertIn("host_0:host_key_verification_is_stale", violations)
        self.assertIn("host_1:host_must_be_unique", violations)
        self.assertIn("host_1:verified_at_must_be_timezone_aware", violations)

    def test_empty_evidence_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_host_key_observation_is_required",), ssh_host_key_evidence_violations([], now=NOW))
        with self.assertRaises(ValueError):
            ssh_host_key_evidence_violations([], now=NOW, maximum_age_seconds=0)


if __name__ == "__main__":
    unittest.main()

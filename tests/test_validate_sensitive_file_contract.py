import unittest

from scripts.validate_sensitive_file_contract import sensitive_file_contract_is_safe, sensitive_file_contract_violations


DIGEST = "a" * 64


class AnsibleSensitiveFileContractGateTests(unittest.TestCase):
    def test_restrictive_root_managed_file_passes(self):
        files = [{"path": "/etc/ssh/sshd_config.d/hardening.conf", "owner": "root", "group": "root", "mode": "0640", "sha256": DIGEST, "managed_by_role": "common"}]
        self.assertTrue(sensitive_file_contract_is_safe(files))

    def test_unapproved_duplicate_and_unsafe_file_fails(self):
        files = [{"path": "/tmp/key", "owner": "deploy", "group": "deploy", "mode": "0644", "sha256": "bad", "managed_by_role": ""}, {"path": "/tmp/key", "owner": "root", "group": "root", "mode": "0600", "sha256": DIGEST, "managed_by_role": "common"}]
        violations = sensitive_file_contract_violations(files)
        self.assertIn("file_0:path_must_be_under_an_allowed_root", violations)
        self.assertIn("file_0:ownership_must_be_root_root", violations)
        self.assertIn("file_0:mode_must_be_restrictive", violations)
        self.assertIn("file_0:sha256_is_invalid", violations)
        self.assertIn("file_0:managed_by_role_is_required", violations)
        self.assertIn("file_1:path_must_be_unique", violations)

    def test_empty_files_and_invalid_root_policy_fail(self):
        self.assertEqual(("at_least_one_sensitive_file_is_required",), sensitive_file_contract_violations([]))
        with self.assertRaises(ValueError):
            sensitive_file_contract_violations([], allowed_roots=("etc/ssh",))


if __name__ == "__main__":
    unittest.main()

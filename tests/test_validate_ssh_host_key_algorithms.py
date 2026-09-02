import unittest

from scripts.validate_ssh_host_key_algorithms import ssh_host_key_algorithm_violations, ssh_host_key_algorithms_are_hardened


class SSHHostKeyAlgorithmContractTests(unittest.TestCase):
    def test_modern_unique_algorithms_pass(self):
        keys = [{"algorithm": "ssh-ed25519"}, {"algorithm": "rsa-sha2-512", "bits": 4096}]
        self.assertTrue(ssh_host_key_algorithms_are_hardened(keys))

    def test_deprecated_duplicate_and_weak_rsa_fail(self):
        keys = [{"algorithm": "ssh-rsa", "bits": 4096}, {"algorithm": "rsa-sha2-256", "bits": 2048}, {"algorithm": "rsa-sha2-256", "bits": 4096}]
        violations = ssh_host_key_algorithm_violations(keys)
        self.assertIn("key_0:deprecated_algorithm_is_forbidden", violations)
        self.assertIn("key_1:rsa_key_size_is_below_minimum", violations)
        self.assertIn("key_2:algorithm_must_be_unique", violations)

    def test_empty_keys_and_invalid_policy_fail(self):
        self.assertIn("at_least_one_host_key_algorithm_is_required", ssh_host_key_algorithm_violations([]))
        with self.assertRaises(ValueError):
            ssh_host_key_algorithm_violations([], minimum_rsa_bits=1024)

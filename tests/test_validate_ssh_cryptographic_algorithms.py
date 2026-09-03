import unittest

from scripts.validate_ssh_cryptographic_algorithms import ssh_cryptographic_algorithm_violations, ssh_cryptographic_algorithms_are_hardened


class SSHCryptographicAlgorithmContractTests(unittest.TestCase):
    def test_modern_effective_algorithm_sets_pass(self):
        config = {"kex_algorithms": ["curve25519-sha256"], "ciphers": ["chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com"], "macs": ["hmac-sha2-512-etm@openssh.com"]}
        self.assertTrue(ssh_cryptographic_algorithms_are_hardened(config))

    def test_legacy_duplicate_and_missing_algorithms_fail(self):
        config = {"kex_algorithms": ["diffie-hellman-group14-sha1"], "ciphers": ["aes128-cbc", "aes128-cbc"], "macs": []}
        violations = ssh_cryptographic_algorithm_violations(config)
        self.assertIn("kex_algorithms:diffie-hellman-group14-sha1:is_not_approved", violations)
        self.assertIn("ciphers_must_be_unique", violations)
        self.assertIn("ciphers:aes128-cbc:is_not_approved", violations)
        self.assertIn("macs_must_be_a_non_empty_string_list", violations)

    def test_invalid_policy_and_shape_fail(self):
        self.assertEqual(("ssh_crypto_config_must_be_an_object",), ssh_cryptographic_algorithm_violations([]))
        with self.assertRaises(ValueError):
            ssh_cryptographic_algorithm_violations({}, approved_kex=frozenset())

import unittest

from scripts.validate_logrotate_policy import logrotate_policy_is_safe, logrotate_policy_violations


class LogrotatePolicyGateTests(unittest.TestCase):
    def test_bounded_compressed_reload_policy_passes(self):
        policies = [{"path": "/var/log/app/app.log", "frequency": "daily", "rotations": 14, "size_mb": 100, "compress": True, "copytruncate": False, "postrotate_reload": True}]
        self.assertTrue(logrotate_policy_is_safe(policies))

    def test_relative_unbounded_uncompressed_and_ambiguous_policy_fails(self):
        policies = [{"path": "var/log/app.log", "frequency": "monthly", "rotations": 2, "size_mb": 2048, "compress": False, "copytruncate": True, "postrotate_reload": True}]
        violations = logrotate_policy_violations(policies)
        self.assertIn("policy_0:path_must_be_absolute", violations)
        self.assertIn("policy_0:frequency_is_invalid", violations)
        self.assertIn("policy_0:rotations_below_minimum", violations)
        self.assertIn("policy_0:size_mb_is_invalid", violations)
        self.assertIn("policy_0:compression_must_be_enabled", violations)
        self.assertIn("policy_0:exactly_one_reopen_strategy_is_required", violations)

    def test_empty_input_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_logrotate_policy_is_required",), logrotate_policy_violations([]))
        with self.assertRaises(ValueError):
            logrotate_policy_violations([], minimum_rotations=0)


if __name__ == "__main__":
    unittest.main()

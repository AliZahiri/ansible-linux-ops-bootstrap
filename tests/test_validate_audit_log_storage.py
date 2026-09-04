import unittest

from scripts.validate_audit_log_storage import audit_log_storage_is_resilient, audit_log_storage_violations


class AuditLogStorageResilienceTests(unittest.TestCase):
    def test_alerting_containment_and_rotation_pass(self):
        config = {"space_left_mib": 2048, "space_left_action": "email", "admin_space_left_action": "single", "disk_full_action": "halt", "disk_error_action": "single", "max_log_file_action": "rotate", "num_logs": 10}
        self.assertTrue(audit_log_storage_is_resilient(config))

    def test_ignore_overwrite_and_low_reserve_fail(self):
        config = {"space_left_mib": 100, "space_left_action": "ignore", "admin_space_left_action": "ignore", "disk_full_action": "ignore", "disk_error_action": "ignore", "max_log_file_action": "keep_logs", "num_logs": 1}
        violations = audit_log_storage_violations(config)
        self.assertIn("audit_space_left_threshold_is_below_minimum", violations)
        self.assertIn("audit_space_left_action_must_alert_or_contain", violations)
        self.assertIn("audit_disk_full_action_must_contain", violations)
        self.assertIn("audit_logs_must_rotate", violations)
        self.assertIn("audit_retained_log_count_is_below_minimum", violations)

    def test_invalid_shape_and_policy_fail(self):
        self.assertEqual(("audit_log_storage_config_must_be_an_object",), audit_log_storage_violations([]))
        with self.assertRaises(ValueError):
            audit_log_storage_violations({}, minimum_num_logs=1)

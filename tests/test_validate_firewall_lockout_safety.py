import unittest
from datetime import datetime, timezone

from scripts.validate_firewall_lockout_safety import firewall_change_is_lockout_safe, firewall_lockout_violations


NOW = datetime(2026, 7, 30, 8, 0, tzinfo=timezone.utc)


class FirewallLockoutSafetyGateTests(unittest.TestCase):
    def test_validated_management_path_with_timed_rollback_passes(self):
        evidence = {"management_source_cidr": "192.0.2.10/32", "ssh_port": 22, "established_session_confirmed": True, "policy_validation_passed": True, "rollback_job_id": "at-2042", "rollback_deadline": "2026-07-30T08:05:00Z"}
        self.assertTrue(firewall_change_is_lockout_safe(evidence, now=NOW))

    def test_invalid_access_path_and_missing_safety_evidence_fail_together(self):
        evidence = {"management_source_cidr": "not-a-cidr", "ssh_port": True, "established_session_confirmed": False, "policy_validation_passed": False, "rollback_job_id": "", "rollback_deadline": "2026-07-30T07:59:00Z"}
        violations = firewall_lockout_violations(evidence, now=NOW)
        self.assertIn("management_source_cidr_is_invalid", violations)
        self.assertIn("ssh_port_is_invalid", violations)
        self.assertIn("established_management_session_must_be_confirmed", violations)
        self.assertIn("firewall_policy_validation_must_pass", violations)
        self.assertIn("rollback_job_id_is_required", violations)
        self.assertIn("rollback_deadline_must_be_in_the_future", violations)

    def test_naive_or_excessive_rollback_window_and_invalid_policy_fail(self):
        evidence = {"management_source_cidr": "192.0.2.10/32", "ssh_port": 22, "established_session_confirmed": True, "policy_validation_passed": True, "rollback_job_id": "at-1", "rollback_deadline": "2026-07-30T09:00:00Z"}
        self.assertIn("rollback_window_exceeds_maximum", firewall_lockout_violations(evidence, now=NOW))
        evidence["rollback_deadline"] = "2026-07-30T08:05:00"
        self.assertIn("rollback_deadline_must_be_timezone_aware", firewall_lockout_violations(evidence, now=NOW))
        with self.assertRaises(ValueError):
            firewall_lockout_violations({}, now=NOW, maximum_rollback_window_seconds=0)


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import datetime, timezone

from scripts.validate_systemd_unit_verification import systemd_unit_is_verified, systemd_unit_verification_violations


NOW = datetime(2026, 7, 30, 8, 0, tzinfo=timezone.utc)


class SystemdUnitVerificationGateTests(unittest.TestCase):
    def test_recent_stable_enabled_unit_passes(self):
        evidence = {"unit": "node-exporter.service", "daemon_reload_completed": True, "enabled": True, "active": True, "result": "success", "restart_count": 0, "observed_at": "2026-07-30T07:59:00Z"}
        self.assertTrue(systemd_unit_is_verified(evidence, now=NOW))

    def test_inactive_unstable_and_stale_unit_reports_all_failures(self):
        evidence = {"unit": "bad unit", "daemon_reload_completed": False, "enabled": False, "active": False, "result": "exit-code", "restart_count": 3, "observed_at": "2026-07-30T07:00:00Z"}
        violations = systemd_unit_verification_violations(evidence, now=NOW)
        self.assertIn("systemd_unit_name_is_invalid", violations)
        self.assertIn("daemon_reload_must_be_confirmed", violations)
        self.assertIn("systemd_unit_must_be_active", violations)
        self.assertIn("restart_count_exceeds_maximum", violations)
        self.assertIn("systemd_observation_is_stale", violations)

    def test_invalid_counter_timestamp_and_policy_fail(self):
        evidence = {"unit": "app.service", "daemon_reload_completed": True, "enabled": True, "active": True, "result": "success", "restart_count": True, "observed_at": "2026-07-30T08:00:00"}
        violations = systemd_unit_verification_violations(evidence, now=NOW)
        self.assertIn("restart_count_must_be_a_non_negative_integer", violations)
        self.assertIn("observed_at_must_be_timezone_aware", violations)
        with self.assertRaises(ValueError):
            systemd_unit_verification_violations({}, now=NOW, maximum_restart_count=-1)


if __name__ == "__main__":
    unittest.main()

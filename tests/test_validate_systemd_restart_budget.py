import unittest

from scripts.validate_systemd_restart_budget import systemd_restart_budget_is_healthy, systemd_restart_budget_violations


class SystemdRestartBudgetEvidenceGateTests(unittest.TestCase):
    def test_active_service_within_restart_budget_passes(self):
        evidence = {"restart_budget": 3, "observed_restarts": 1, "observation_window_minutes": 15, "unit_active": True, "observed_at": "2026-08-20T12:00:00Z"}
        self.assertTrue(systemd_restart_budget_is_healthy(evidence))

    def test_excessive_or_unhealthy_service_fails(self):
        violations = systemd_restart_budget_violations({"restart_budget": 1, "observed_restarts": 2, "observation_window_minutes": 0, "unit_active": False, "observed_at": "2026-08-20T12:00:00"})
        self.assertEqual(violations, ("observation_window_minutes_must_be_positive", "observed_restarts_exceed_budget", "unit_must_be_active", "observed_at_must_be_timezone_aware"))

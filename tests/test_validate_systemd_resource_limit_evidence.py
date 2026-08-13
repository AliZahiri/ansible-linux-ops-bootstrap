import unittest
from datetime import datetime, timezone

from scripts.validate_systemd_resource_limit_evidence import systemd_resource_limit_evidence_violations, systemd_resource_limits_are_verified


NOW = datetime(2026, 8, 13, 6, 0, tzinfo=timezone.utc)


def evidence() -> dict[str, object]:
    return {"unit": "node-exporter.service", "active": True, "configuration_read": True, "memory_max_bytes": 268435456, "tasks_max": 256, "limit_nofile": 4096, "observed_at": "2026-08-13T05:55:00Z"}


class SystemdResourceLimitEvidenceGateTests(unittest.TestCase):
    def test_fresh_active_service_limit_evidence_passes(self):
        self.assertTrue(systemd_resource_limits_are_verified(evidence(), now=NOW))

    def test_inactive_invalid_and_stale_evidence_fails(self):
        candidate = evidence()
        candidate.update({"unit": "../unsafe", "active": False, "configuration_read": False, "memory_max_bytes": 0, "tasks_max": False, "limit_nofile": 128, "observed_at": "2026-08-13T04:00:00Z"})
        violations = systemd_resource_limit_evidence_violations(candidate, now=NOW)
        self.assertIn("systemd_unit_name_is_invalid", violations)
        self.assertIn("systemd_unit_must_be_active", violations)
        self.assertIn("systemd_configuration_must_be_read", violations)
        self.assertIn("memory_max_bytes_must_be_positive", violations)
        self.assertIn("tasks_max_must_be_positive", violations)
        self.assertIn("limit_nofile_is_below_minimum", violations)
        self.assertIn("resource_limit_evidence_is_stale", violations)

    def test_invalid_policy_and_naive_clock_fail(self):
        with self.assertRaises(ValueError):
            systemd_resource_limit_evidence_violations({}, now=NOW, minimum_nofile=0)
        with self.assertRaises(ValueError):
            systemd_resource_limit_evidence_violations({}, now=datetime(2026, 8, 13, 6, 0))


if __name__ == "__main__":
    unittest.main()

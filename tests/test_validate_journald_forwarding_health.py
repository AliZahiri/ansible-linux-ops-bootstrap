import unittest
from datetime import datetime, timezone

from scripts.validate_journald_forwarding_health import journald_forwarding_health_violations, journald_forwarding_is_healthy


NOW = datetime(2026, 8, 11, 8, 0, tzinfo=timezone.utc)


class JournaldForwardingHealthEvidenceGateTests(unittest.TestCase):
    def test_fresh_enabled_forwarding_passes(self):
        observations = [{"host": "app-01", "forwarding_enabled": True, "delivered_at": "2026-08-11T07:55:00Z", "backlog_count": 0}]
        self.assertTrue(journald_forwarding_is_healthy(observations, now=NOW))

    def test_duplicate_disabled_stale_and_negative_observation_fails(self):
        observations = [{"host": "app-01", "forwarding_enabled": False, "delivered_at": "2026-08-11T06:00:00Z", "backlog_count": -1}, {"host": "app-01", "forwarding_enabled": True, "delivered_at": "2026-08-11T07:55:00Z", "backlog_count": 0}]
        violations = journald_forwarding_health_violations(observations, now=NOW)
        self.assertIn("observation_0:forwarding_must_be_enabled", violations)
        self.assertIn("observation_0:delivery_is_not_fresh", violations)
        self.assertIn("observation_0:backlog_count_must_be_non_negative", violations)
        self.assertIn("observation_1:host_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()

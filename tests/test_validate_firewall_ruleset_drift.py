import unittest
from datetime import datetime, timezone

from scripts.validate_firewall_ruleset_drift import firewall_ruleset_drift_violations, firewall_ruleset_matches


NOW = datetime(2026, 9, 1, 1, 0, tzinfo=timezone.utc)


class FirewallRulesetDriftTests(unittest.TestCase):
    def test_fresh_exact_default_deny_ruleset_passes(self):
        observation = {"default_input_policy": "drop", "allowed_services": ["ssh", "node-exporter"], "captured_at": "2026-09-01T00:30:00Z", "ruleset_digest": "sha256:abc"}
        self.assertTrue(firewall_ruleset_matches(["ssh", "node-exporter"], observation, now=NOW))

    def test_open_policy_missing_and_unexpected_services_fail(self):
        observation = {"default_input_policy": "accept", "allowed_services": ["ssh", "mysql"], "captured_at": "2026-08-31T20:00:00Z", "ruleset_digest": "sha256:old"}
        violations = firewall_ruleset_drift_violations(["ssh", "node-exporter"], observation, now=NOW)
        self.assertIn("default_input_policy_must_deny", violations)
        self.assertIn("required_firewall_services_are_missing", violations)
        self.assertIn("unexpected_firewall_services_are_allowed", violations)
        self.assertIn("firewall_observation_is_stale_or_future_dated", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            firewall_ruleset_drift_violations([], {}, now=NOW, maximum_age_seconds=0)

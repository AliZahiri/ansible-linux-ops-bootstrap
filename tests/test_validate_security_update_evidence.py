import unittest
from datetime import datetime, timezone

from scripts.validate_security_update_evidence import security_update_evidence_is_healthy, security_update_evidence_violations


NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


class SecurityUpdateRuntimeEvidenceTests(unittest.TestCase):
    def test_fresh_fully_applied_security_updates_pass(self):
        hosts = [{"host_id": "web-01", "observed_at": "2026-08-28T11:30:00Z", "pending_security_updates": 0, "failed_security_updates": 0, "reboot_required": False}]
        self.assertTrue(security_update_evidence_is_healthy(hosts, now=NOW))

    def test_stale_pending_failed_and_reboot_required_evidence_fails(self):
        hosts = [{"host_id": "web-01", "observed_at": "2026-08-26T08:00:00Z", "pending_security_updates": 2, "failed_security_updates": 1, "reboot_required": True}]
        violations = security_update_evidence_violations(hosts, now=NOW)
        self.assertIn("host_0:evidence_is_stale_or_future_dated", violations)
        self.assertIn("host_0:pending_security_updates_exceeds_budget", violations)
        self.assertIn("host_0:failed_security_updates_exceeds_budget", violations)
        self.assertIn("host_0:security_update_reboot_is_pending", violations)

    def test_duplicate_host_and_malformed_counts_fail(self):
        hosts = [{"host_id": "db-01", "observed_at": "2026-08-28T11:00:00Z", "pending_security_updates": 0, "failed_security_updates": 0, "reboot_required": False}, {"host_id": "db-01", "observed_at": "naive", "pending_security_updates": True, "failed_security_updates": -1, "reboot_required": "no"}]
        violations = security_update_evidence_violations(hosts, now=NOW)
        self.assertIn("host_1:host_id_must_be_unique", violations)
        self.assertIn("host_1:pending_security_updates_must_be_non_negative", violations)
        self.assertIn("host_1:reboot_required_must_be_boolean", violations)

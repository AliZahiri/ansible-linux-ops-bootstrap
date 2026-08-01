import unittest
from datetime import datetime, timezone

from scripts.validate_audit_log_forwarding import audit_log_forwarding_is_ready, audit_log_forwarding_violations


NOW = datetime(2026, 8, 1, 12, 0, tzinfo=timezone.utc)


class AuditLogForwardingEvidenceGateTests(unittest.TestCase):
    def test_recent_tls_verified_disk_queued_delivery_passes(self):
        evidence = {"service_active": True, "tls_peer_verified": True, "disk_queue_enabled": True, "destination_count": 1, "dropped_events": 0, "last_delivery_at": "2026-08-01T11:59:00Z"}
        self.assertTrue(audit_log_forwarding_is_ready(evidence, now=NOW))

    def test_inactive_unverified_dropping_and_stale_forwarder_fails(self):
        evidence = {"service_active": False, "tls_peer_verified": False, "disk_queue_enabled": False, "destination_count": 0, "dropped_events": 2, "last_delivery_at": "2026-08-01T10:00:00Z"}
        violations = audit_log_forwarding_violations(evidence, now=NOW)
        self.assertIn("audit_forwarder_service_must_be_active", violations)
        self.assertIn("audit_forwarder_tls_peer_must_be_verified", violations)
        self.assertIn("audit_events_must_not_be_dropped", violations)
        self.assertIn("audit_delivery_observation_is_stale", violations)

    def test_naive_timestamp_and_invalid_policy_fail(self):
        violations = audit_log_forwarding_violations({"last_delivery_at": "2026-08-01T12:00:00"}, now=NOW)
        self.assertIn("last_delivery_at_must_be_timezone_aware", violations)
        with self.assertRaises(ValueError):
            audit_log_forwarding_violations({}, now=NOW, maximum_delivery_age_seconds=0)


if __name__ == "__main__":
    unittest.main()

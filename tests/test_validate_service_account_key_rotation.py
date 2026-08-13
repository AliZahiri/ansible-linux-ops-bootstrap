import unittest
from datetime import datetime, timezone

from scripts.validate_service_account_key_rotation import service_account_key_rotation_is_current, service_account_key_rotation_violations


NOW = datetime(2026, 8, 13, 6, 0, tzinfo=timezone.utc)


class ServiceAccountKeyRotationEvidenceGateTests(unittest.TestCase):
    def test_fresh_unexpired_key_evidence_passes(self):
        records = [{"service_account": "backup", "key_id": "key-2026-08", "rotated_at": "2026-08-01T00:00:00Z", "expires_at": "2026-09-01T00:00:00Z"}]
        self.assertTrue(service_account_key_rotation_is_current(records, now=NOW))

    def test_duplicate_stale_and_expired_evidence_fails(self):
        records = [{"service_account": "backup", "key_id": "", "rotated_at": "2026-01-01T00:00:00Z", "expires_at": "2026-08-01T00:00:00Z"}, {"service_account": "backup", "key_id": "key-2", "rotated_at": "2026-08-01T00:00:00Z", "expires_at": "2026-09-01T00:00:00Z"}]
        violations = service_account_key_rotation_violations(records, now=NOW)
        self.assertIn("record_0:key_id_is_required", violations)
        self.assertIn("record_0:rotation_is_not_fresh", violations)
        self.assertIn("record_0:key_must_not_be_expired", violations)
        self.assertIn("record_1:service_account_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()

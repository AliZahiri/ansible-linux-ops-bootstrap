import unittest
from datetime import datetime, timezone

from scripts.validate_ssh_authorized_key_provenance import (
    ssh_authorized_key_provenance_is_current,
    ssh_authorized_key_provenance_violations,
)


NOW = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)
FINGERPRINT = "SHA256:" + "a" * 43


class SshAuthorizedKeyProvenanceTests(unittest.TestCase):
    def test_recent_non_root_key_metadata_passes(self):
        entries = [{"account": "deploy", "fingerprint": FINGERPRINT, "change_ticket": "OPS-42", "reviewed_at": "2026-09-20T12:00:00Z"}]
        self.assertTrue(ssh_authorized_key_provenance_is_current(entries, now=NOW))

    def test_root_bad_ticket_duplicate_and_stale_review_fail(self):
        entries = [
            {"account": "root", "fingerprint": FINGERPRINT, "change_ticket": "bad", "reviewed_at": "2025-01-01T00:00:00Z"},
            {"account": "root", "fingerprint": FINGERPRINT, "change_ticket": "OPS-43", "reviewed_at": "2026-09-20T12:00:00Z"},
        ]
        violations = ssh_authorized_key_provenance_violations(entries, now=NOW)
        self.assertIn("entry_0:account_must_be_a_non_root_identity", violations)
        self.assertIn("entry_0:change_ticket_is_invalid", violations)
        self.assertIn("entry_0:review_is_stale_or_future_dated", violations)
        self.assertIn("entry_1:account_fingerprint_assignment_must_be_unique", violations)

    def test_invalid_policy_fails_fast(self):
        with self.assertRaises(ValueError):
            ssh_authorized_key_provenance_violations([], now=datetime(2026, 10, 19), maximum_review_age_seconds=0)

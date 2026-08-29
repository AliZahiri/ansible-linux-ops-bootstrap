import unittest
from datetime import datetime, timezone

from scripts.validate_temporary_privileged_accounts import temporary_privileged_account_violations, temporary_privileged_accounts_are_safe


NOW = datetime(2026, 8, 29, 12, 0, tzinfo=timezone.utc)


class TemporaryPrivilegedAccountExpiryTests(unittest.TestCase):
    def test_approved_key_only_bounded_account_passes(self):
        accounts = [{"username": "incident-admin", "approval_ticket": "INC-42", "approved_by": "platform-lead", "password_locked": True, "ssh_key_count": 1, "expires_at": "2026-08-29T18:00:00Z"}]
        self.assertTrue(temporary_privileged_accounts_are_safe(accounts, now=NOW))

    def test_unapproved_password_account_with_long_expiry_fails(self):
        accounts = [{"username": "debug-admin", "approval_ticket": "", "approved_by": "", "password_locked": False, "ssh_key_count": 0, "expires_at": "2026-09-02T12:00:00Z"}]
        violations = temporary_privileged_account_violations(accounts, now=NOW)
        self.assertIn("account_0:approval_ticket_is_required", violations)
        self.assertIn("account_0:password_must_be_locked", violations)
        self.assertIn("account_0:ssh_key_count_must_be_positive", violations)
        self.assertIn("account_0:temporary_access_exceeds_validity_window", violations)

    def test_expired_and_invalid_policy_fail(self):
        accounts = [{"username": "old-admin", "approval_ticket": "INC-1", "approved_by": "lead", "password_locked": True, "ssh_key_count": 1, "expires_at": "2026-08-29T11:00:00Z"}]
        self.assertIn("account_0:temporary_access_is_expired", temporary_privileged_account_violations(accounts, now=NOW))
        with self.assertRaises(ValueError):
            temporary_privileged_account_violations([], now=NOW, maximum_validity_seconds=0)

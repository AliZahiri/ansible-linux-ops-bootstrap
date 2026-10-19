import unittest
from datetime import datetime, timezone
from scripts.validate_ssh_authorized_key_expiry import ssh_authorized_key_expiry_violations
NOW=datetime(2026,10,19,12,tzinfo=timezone.utc)
class SshAuthorizedKeyExpiryTests(unittest.TestCase):
    def test_short_lived_key_passes(self): self.assertEqual((), ssh_authorized_key_expiry_violations([{'account':'deploy','fingerprint':'SHA256:abc','expires_at':'2026-11-01T12:00:00Z'}], now=NOW))
    def test_duplicate_and_expired_key_fail(self):
        entries=[{'account':'deploy','fingerprint':'SHA256:abc','expires_at':'2026-10-18T12:00:00Z'}]*2
        violations=ssh_authorized_key_expiry_violations(entries, now=NOW)
        self.assertIn('entry_0:expiry_is_missing_expired_or_exceeds_maximum_lifetime', violations); self.assertIn('entry_1:account_fingerprint_assignment_must_be_unique', violations)

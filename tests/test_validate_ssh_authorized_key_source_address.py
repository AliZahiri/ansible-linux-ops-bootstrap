import unittest
from scripts.validate_ssh_authorized_key_source_address import ssh_authorized_key_source_address_violations
class SshAuthorizedKeySourceAddressTests(unittest.TestCase):
    def test_bounded_unique_cidrs_pass(self): self.assertEqual((), ssh_authorized_key_source_address_violations([{'source_addresses':['10.0.0.0/24','2001:db8::/64']}]))
    def test_unrestricted_invalid_and_duplicate_cidrs_fail(self):
        violations=ssh_authorized_key_source_address_violations([{'source_addresses':['0.0.0.0/0','bad','10.0.0.0/24','10.0.0.0/24']}])
        self.assertIn('entry_0:source_address_must_be_a_bounded_cidr', violations); self.assertIn('entry_0:source_addresses_must_be_unique', violations)

import unittest
from scripts.validate_systemd_runtime_identity import systemd_runtime_identity_is_safe, systemd_runtime_identity_violations

class SystemdRuntimeIdentityContractTests(unittest.TestCase):
    def test_non_root_identity_passes(self): self.assertTrue(systemd_runtime_identity_is_safe({"User": "app", "Group": "app", "SupplementaryGroups": ["logs"]}))
    def test_root_and_duplicate_group_fail(self):
        violations = systemd_runtime_identity_violations({"User": "root", "Group": "", "SupplementaryGroups": ["ops", "ops"]})
        self.assertIn("User_must_be_a_non_root_identity", violations); self.assertIn("Group_must_be_a_non_root_identity", violations); self.assertIn("SupplementaryGroups_must_be_unique_non_empty_strings", violations)

if __name__ == "__main__": unittest.main()

import unittest

from scripts.validate_systemd_service_hardening import systemd_service_hardening_violations, systemd_service_is_hardened


class SystemdServiceHardeningContractTests(unittest.TestCase):
    def test_hardened_service_with_required_state_path_passes(self):
        settings = {"NoNewPrivileges": True, "PrivateTmp": True, "ProtectHome": True, "ProtectSystem": "strict", "ReadWritePaths": ["/var/lib/example"]}
        self.assertTrue(systemd_service_is_hardened(settings, required_read_write_paths=frozenset({"/var/lib/example"})))

    def test_missing_isolation_and_relative_write_path_fail(self):
        settings = {"NoNewPrivileges": False, "PrivateTmp": False, "ProtectHome": False, "ProtectSystem": "no", "ReadWritePaths": ["var/lib/example"]}
        violations = systemd_service_hardening_violations(settings, required_read_write_paths=frozenset({"/var/lib/example"}))
        self.assertIn("NoNewPrivileges_must_be_enabled", violations)
        self.assertIn("ProtectSystem_must_be_full_or_strict", violations)
        self.assertIn("ReadWritePaths_must_be_a_list_of_absolute_paths", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            systemd_service_hardening_violations({}, required_read_write_paths=frozenset({"relative"}))

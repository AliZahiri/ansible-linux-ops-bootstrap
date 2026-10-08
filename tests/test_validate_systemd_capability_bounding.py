import unittest

from scripts.validate_systemd_capability_bounding import systemd_capability_bounding_is_safe, systemd_capability_bounding_violations


class SystemdCapabilityBoundingContractTests(unittest.TestCase):
    def test_bounded_non_ambient_service_passes(self):
        settings = {"CapabilityBoundingSet": ["CAP_NET_BIND_SERVICE"], "AmbientCapabilities": [], "NoNewPrivileges": True}
        self.assertTrue(systemd_capability_bounding_is_safe(settings))

    def test_forbidden_capability_and_ambient_privilege_fail(self):
        settings = {"CapabilityBoundingSet": ["CAP_SYS_ADMIN"], "AmbientCapabilities": ["CAP_NET_ADMIN"], "NoNewPrivileges": False}
        violations = systemd_capability_bounding_violations(settings)
        self.assertIn("CapabilityBoundingSet_contains_duplicate_or_forbidden_capability", violations)
        self.assertIn("AmbientCapabilities_must_be_empty", violations)
        self.assertIn("NoNewPrivileges_must_be_enabled", violations)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UnattendedUpgradesTemplateTests(unittest.TestCase):
    def test_template_limits_updates_to_security_origin_and_reboot_policy(self):
        content = (ROOT / "roles/common/templates/50unattended-upgrades.j2").read_text(encoding="utf-8")

        self.assertIn("${distro_codename}-security", content)
        self.assertIn("Automatic-Reboot", content)
        self.assertIn("unattended_reboot_time", content)

    def test_template_supports_cleanup_and_package_blacklist(self):
        content = (ROOT / "roles/common/templates/50unattended-upgrades.j2").read_text(encoding="utf-8")

        self.assertIn("Remove-Unused-Dependencies", content)
        self.assertIn("Package-Blacklist", content)
        self.assertIn("unattended_package_blacklist", content)


if __name__ == "__main__":
    unittest.main()

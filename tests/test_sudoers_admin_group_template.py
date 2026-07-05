import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SudoersAdminGroupTemplateTests(unittest.TestCase):
    def test_sudoers_template_uses_group_and_visudo_hint(self):
        content = (ROOT / "roles/common/templates/sudoers-admin-group.j2").read_text(encoding="utf-8")

        self.assertIn("visudo -cf", content)
        self.assertIn("sudo_admin_group", content)
        self.assertIn("ALL=(ALL:ALL)", content)


if __name__ == "__main__":
    unittest.main()

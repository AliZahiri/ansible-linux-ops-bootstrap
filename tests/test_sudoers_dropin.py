import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SudoersDropinTests(unittest.TestCase):
    def test_sudoers_dropin_limits_commands(self):
        content = (ROOT / "roles/common/templates/sudoers-deploy.j2").read_text(encoding="utf-8")

        self.assertIn("{{ deploy_user }}", content)
        self.assertIn("/usr/bin/systemctl reload nginx", content)
        self.assertNotIn("NOPASSWD: ALL", content)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SshdAllowedUsersTemplateTests(unittest.TestCase):
    def test_sshd_allowed_users_template_restricts_login(self):
        content = (ROOT / "roles/common/templates/sshd-allowed-users.conf.j2").read_text(encoding="utf-8")

        self.assertIn("PermitRootLogin no", content)
        self.assertIn("PasswordAuthentication", content)
        self.assertIn("ssh_allowed_users", content)


if __name__ == "__main__":
    unittest.main()

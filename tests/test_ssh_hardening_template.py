import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SshHardeningTemplateTests(unittest.TestCase):
    def test_template_disables_password_and_root_login(self):
        template = ROOT / "roles/common/templates/sshd-hardening.conf.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("PasswordAuthentication no", content)
        self.assertIn("PermitRootLogin no", content)

    def test_template_keeps_key_authentication_enabled(self):
        template = ROOT / "roles/common/templates/sshd-hardening.conf.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("PubkeyAuthentication yes", content)


if __name__ == "__main__":
    unittest.main()

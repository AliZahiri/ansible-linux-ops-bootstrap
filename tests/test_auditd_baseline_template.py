import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AuditdBaselineTemplateTests(unittest.TestCase):
    def test_auditd_template_watches_sensitive_paths(self):
        content = (ROOT / "roles/common/templates/auditd-baseline.rules.j2").read_text(encoding="utf-8")

        self.assertIn("/etc/ssh/sshd_config", content)
        self.assertIn("/etc/sudoers", content)
        self.assertIn("/etc/passwd", content)


if __name__ == "__main__":
    unittest.main()

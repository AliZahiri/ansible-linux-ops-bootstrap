import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SystemdServiceTemplateTests(unittest.TestCase):
    def test_service_template_has_restart_and_environment_file(self):
        content = (ROOT / "roles/common/templates/platform-service.service.j2").read_text(encoding="utf-8")

        self.assertIn("Restart=on-failure", content)
        self.assertIn("EnvironmentFile={{ service_environment_file }}", content)
        self.assertIn("WantedBy=multi-user.target", content)


if __name__ == "__main__":
    unittest.main()

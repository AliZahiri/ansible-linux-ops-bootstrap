import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SystemdRestartSafetyTemplateTests(unittest.TestCase):
    def test_restart_policy_is_bounded(self):
        content = (ROOT / "roles/common/templates/systemd-restart-safety.conf.j2").read_text(encoding="utf-8")

        self.assertIn("Restart=on-failure", content)
        self.assertIn("RestartSec", content)
        self.assertIn("StartLimitIntervalSec", content)
        self.assertIn("StartLimitBurst", content)


if __name__ == "__main__":
    unittest.main()

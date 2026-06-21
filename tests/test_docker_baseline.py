import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DockerBaselineTests(unittest.TestCase):
    def test_daemon_template_enables_live_restore_and_log_rotation(self):
        template = ROOT / "roles/docker/templates/daemon.json.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn('"live-restore": true', content)
        self.assertIn('"max-size": "100m"', content)
        self.assertIn('"max-file": "3"', content)

    def test_baseline_task_installs_daemon_config(self):
        task = ROOT / "roles/docker/tasks/baseline.yml"
        content = task.read_text(encoding="utf-8")

        self.assertIn("daemon.json.j2", content)
        self.assertIn("/etc/docker/daemon.json", content)


if __name__ == "__main__":
    unittest.main()

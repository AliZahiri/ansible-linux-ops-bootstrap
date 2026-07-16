import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SystemdResourceLimitsTemplateTests(unittest.TestCase):
    def test_template_declares_memory_file_and_task_limits(self):
        content = (ROOT / "roles/common/templates/systemd-resource-limits.conf.j2").read_text(encoding="utf-8")

        self.assertIn("MemoryMax", content)
        self.assertIn("LimitNOFILE", content)
        self.assertIn("TasksMax", content)


if __name__ == "__main__":
    unittest.main()

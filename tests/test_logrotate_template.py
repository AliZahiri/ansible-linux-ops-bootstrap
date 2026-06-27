import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LogrotateTemplateTests(unittest.TestCase):
    def test_logrotate_template_sets_rotation_and_compression(self):
        content = (ROOT / "roles/common/templates/platform-logrotate.j2").read_text(encoding="utf-8")

        self.assertIn("daily", content)
        self.assertIn("compress", content)
        self.assertIn("missingok", content)


if __name__ == "__main__":
    unittest.main()

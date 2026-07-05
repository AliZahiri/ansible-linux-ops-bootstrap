import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class JournaldRetentionTemplateTests(unittest.TestCase):
    def test_journald_template_controls_retention(self):
        content = (ROOT / "roles/common/templates/journald.conf.j2").read_text(encoding="utf-8")

        self.assertIn("Storage=persistent", content)
        self.assertIn("Compress=yes", content)
        self.assertIn("SystemMaxUse", content)
        self.assertIn("MaxRetentionSec", content)


if __name__ == "__main__":
    unittest.main()

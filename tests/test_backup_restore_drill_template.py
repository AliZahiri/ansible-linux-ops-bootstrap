import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BackupRestoreDrillTemplateTests(unittest.TestCase):
    def test_restore_drill_template_has_guardrails(self):
        content = (ROOT / "roles/common/templates/backup-restore-drill.sh.j2").read_text(encoding="utf-8")

        self.assertIn("backup manifest path is required", content)
        self.assertIn("refusing to restore into filesystem root", content)
        self.assertIn("DRY_RUN", content)


if __name__ == "__main__":
    unittest.main()

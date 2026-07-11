import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupHealthcheckTemplateTests(unittest.TestCase):
    def test_template_requires_artifact_and_writes_status(self):
        content = (ROOT / "roles/backup/templates/backup-healthcheck.sh.j2").read_text(encoding="utf-8")

        self.assertIn("BACKUP_ARTIFACT is required", content)
        self.assertIn("last-success.txt", content)
        self.assertIn("completed_at", content)
        self.assertNotIn("PGPASSWORD", content)


if __name__ == "__main__":
    unittest.main()

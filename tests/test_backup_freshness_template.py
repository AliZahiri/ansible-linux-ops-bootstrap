import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupFreshnessTemplateTests(unittest.TestCase):
    def test_template_checks_artifact_age_without_credentials(self):
        content = (ROOT / "roles/backup/templates/check-backup-freshness.sh.j2").read_text(encoding="utf-8")

        self.assertIn("BACKUP_ARTIFACT is required", content)
        self.assertIn("backup_max_age_minutes", content)
        self.assertIn("backup is stale", content)
        self.assertNotIn("PGPASSWORD", content)


if __name__ == "__main__":
    unittest.main()

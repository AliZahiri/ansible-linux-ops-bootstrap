import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupRetentionTemplateTests(unittest.TestCase):
    def test_retention_template_has_positive_defaults_and_encryption(self):
        content = (ROOT / "roles/backup/templates/backup-retention.env.j2").read_text(encoding="utf-8")

        self.assertIn("default(14)", content)
        self.assertIn("default(6)", content)
        self.assertIn("BACKUP_ENCRYPTION_REQUIRED=true", content)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupRestoreChecksumTemplateTests(unittest.TestCase):
    def test_template_requires_inputs_and_verifies_sha256(self):
        content = (ROOT / "roles/backup/templates/verify-backup-checksum.sh.j2").read_text(encoding="utf-8")

        self.assertIn("BACKUP_ARTIFACT is required", content)
        self.assertIn("BACKUP_CHECKSUM_FILE is required", content)
        self.assertIn("sha256sum --check", content)
        self.assertNotIn("PGPASSWORD", content)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupArtifactPermissionTemplateTests(unittest.TestCase):
    def test_template_uses_restrictive_modes_without_credentials(self):
        content = (ROOT / "roles/backup/templates/backup-artifact-permissions.sh.j2").read_text(encoding="utf-8")

        self.assertIn("BACKUP_ARTIFACT is required", content)
        self.assertIn("-m 0750", content)
        self.assertIn("chmod 0640", content)
        self.assertNotIn("PGPASSWORD", content)


if __name__ == "__main__":
    unittest.main()

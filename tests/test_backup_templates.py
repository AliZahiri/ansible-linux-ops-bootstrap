import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BackupTemplateTests(unittest.TestCase):
    def test_restore_template_requires_restore_file(self):
        template = ROOT / "roles/backup/templates/restore-postgres.sh.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("RESTORE_FILE is required", content)
        self.assertIn("pg_restore", content)

    def test_restore_template_uses_safe_restore_flags(self):
        template = ROOT / "roles/backup/templates/restore-postgres.sh.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("--clean", content)
        self.assertIn("--if-exists", content)
        self.assertIn("--no-owner", content)


if __name__ == "__main__":
    unittest.main()

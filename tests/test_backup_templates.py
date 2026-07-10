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

    def test_restore_verification_template_documents_required_variables(self):
        template = ROOT / "roles/backup/templates/verify-postgres-restore.sh.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("POSTGRES_HOST is required", content)
        self.assertIn("POSTGRES_DB is required", content)
        self.assertIn("POSTGRES_USER is required", content)
        self.assertIn("PGPASSWORD is required", content)
        self.assertIn("psql", content)
        self.assertIn("ON_ERROR_STOP=1", content)
        self.assertIn("backup_restore_verify_query", content)
        self.assertIn("PGCONNECT_TIMEOUT", content)
        self.assertIn("backup_restore_verify_connect_timeout_seconds", content)

    def test_restore_verification_task_is_flag_gated(self):
        tasks = (ROOT / "roles/backup/tasks/main.yml").read_text(encoding="utf-8")

        self.assertIn("verify-postgres-restore.sh.j2", tasks)
        self.assertIn("backup_restore_verify_enabled | bool", tasks)

    def test_backup_role_defaults_expose_restore_verification_settings(self):
        defaults = (ROOT / "roles/backup/defaults/main.yml").read_text(encoding="utf-8")

        self.assertIn("backup_restore_verify_enabled: false", defaults)
        self.assertIn('backup_restore_verify_query: "select 1"', defaults)
        self.assertIn("backup_restore_verify_connect_timeout_seconds: 5", defaults)


if __name__ == "__main__":
    unittest.main()

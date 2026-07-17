import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RestoreDrillEvidenceTemplateTests(unittest.TestCase):
    def test_template_records_integrity_timing_and_application_checks(self):
        content = (ROOT / "roles/backup/templates/restore-drill-evidence.json.j2").read_text(encoding="utf-8")

        for field in ("backup_id", "checksum_verified", "started_at", "completed_at", "application_verification_passed"):
            self.assertIn(f'"{field}"', content)

    def test_template_does_not_embed_secret_fields(self):
        content = (ROOT / "roles/backup/templates/restore-drill-evidence.json.j2").read_text(encoding="utf-8").lower()
        self.assertNotIn("password", content)
        self.assertNotIn("private_key", content)


if __name__ == "__main__":
    unittest.main()

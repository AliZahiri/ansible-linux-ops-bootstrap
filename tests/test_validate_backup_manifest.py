import unittest

from scripts.validate_backup_manifest import backup_manifest_is_valid, backup_manifest_violations


def valid_manifest():
    return {"backup_id": "postgres-20260724T120000Z", "artifact_name": "postgres.sql.gz", "created_at": "2026-07-24T12:00:00Z", "size_bytes": 4096, "sha256": "a" * 64}


class BackupArtifactManifestTests(unittest.TestCase):
    def test_complete_manifest_passes(self):
        self.assertTrue(backup_manifest_is_valid(valid_manifest()))

    def test_path_timestamp_size_and_digest_failures_are_partitioned(self):
        manifest = valid_manifest()
        manifest.update({"artifact_name": "../postgres.sql.gz", "created_at": "2026-07-24T12:00:00", "size_bytes": True, "sha256": "short"})

        violations = backup_manifest_violations(manifest)

        self.assertIn("artifact_name_must_not_contain_a_path", violations)
        self.assertIn("created_at_must_be_timezone_aware", violations)
        self.assertIn("size_bytes_must_be_a_positive_integer", violations)
        self.assertIn("sha256_must_be_a_complete_digest", violations)

    def test_unbounded_or_unsafe_backup_identifier_fails(self):
        manifest = valid_manifest()
        manifest["backup_id"] = "../../outside"

        self.assertEqual(("backup_id_is_invalid",), backup_manifest_violations(manifest))


if __name__ == "__main__":
    unittest.main()

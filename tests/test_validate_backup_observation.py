import unittest

from scripts.validate_backup_observation import backup_observation_matches_manifest, backup_observation_violations


def manifest():
    return {"backup_id": "postgres-20260725T120000Z", "artifact_name": "postgres.sql.gz", "created_at": "2026-07-25T12:00:00Z", "size_bytes": 4096, "sha256": "a" * 64}


class BackupArtifactObservationTests(unittest.TestCase):
    def test_matching_observation_passes(self):
        self.assertTrue(backup_observation_matches_manifest(manifest=manifest(), observed_size_bytes=4096, observed_sha256="A" * 64))

    def test_size_and_digest_mismatches_are_reported(self):
        violations = backup_observation_violations(manifest=manifest(), observed_size_bytes=2048, observed_sha256="b" * 64)
        self.assertIn("observed_size_does_not_match_manifest", violations)
        self.assertIn("observed_sha256_does_not_match_manifest", violations)

    def test_manifest_and_observation_shape_failures_remain_separate(self):
        invalid = manifest()
        invalid["backup_id"] = "../unsafe"
        violations = backup_observation_violations(manifest=invalid, observed_size_bytes=True, observed_sha256="short")
        self.assertIn("manifest:backup_id_is_invalid", violations)
        self.assertIn("observed_size_bytes_must_be_a_positive_integer", violations)
        self.assertIn("observed_sha256_must_be_a_complete_digest", violations)


if __name__ == "__main__":
    unittest.main()

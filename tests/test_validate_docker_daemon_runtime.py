import unittest
from datetime import datetime, timezone

from scripts.validate_docker_daemon_runtime import docker_daemon_runtime_is_safe, docker_daemon_runtime_violations


NOW = datetime(2026, 8, 14, 6, 0, tzinfo=timezone.utc)
EVIDENCE = {"live_restore": True, "rootless": False, "userns_remap": True, "log_driver": "local", "log_max_size_mb": 20, "log_max_files": 5, "observed_at": "2026-08-14T05:55:00Z"}


class DockerDaemonRuntimeEvidenceGateTests(unittest.TestCase):
    def test_fresh_hardened_daemon_passes(self):
        self.assertTrue(docker_daemon_runtime_is_safe(EVIDENCE, now=NOW))

    def test_unsafe_and_stale_daemon_fails(self):
        violations = docker_daemon_runtime_violations({**EVIDENCE, "live_restore": False, "userns_remap": False, "log_driver": "none", "log_max_size_mb": 0, "log_max_files": 1, "observed_at": "2026-08-14T04:00:00Z"}, now=NOW)
        self.assertIn("live_restore_must_be_enabled", violations)
        self.assertIn("rootless_or_userns_remap_is_required", violations)
        self.assertIn("log_driver_must_be_supported", violations)
        self.assertIn("log_max_size_mb_must_be_between_1_and_100", violations)
        self.assertIn("log_max_files_must_be_between_2_and_20", violations)
        self.assertIn("daemon_evidence_is_not_fresh", violations)


if __name__ == "__main__":
    unittest.main()

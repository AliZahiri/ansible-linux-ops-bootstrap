import unittest
from datetime import datetime, timezone

from scripts.validate_core_dump_policy import core_dump_policy_is_hardened, core_dump_policy_violations


NOW = datetime(2026, 9, 2, 4, 0, tzinfo=timezone.utc)


class LinuxCoreDumpPolicyEvidenceTests(unittest.TestCase):
    def test_fresh_effective_disabled_policy_passes(self):
        evidence = {"systemd_coredump_storage": "none", "process_core_limit_bytes": 0, "fs_suid_dumpable": 0, "kernel_core_pattern": "|/bin/false", "observed_at": "2026-09-02T03:30:00Z"}
        self.assertTrue(core_dump_policy_is_hardened(evidence, now=NOW))

    def test_persistent_dumping_and_stale_evidence_fail(self):
        evidence = {"systemd_coredump_storage": "external", "process_core_limit_bytes": 1024, "fs_suid_dumpable": 2, "kernel_core_pattern": "core.%p", "observed_at": "2026-09-01T00:00:00Z"}
        violations = core_dump_policy_violations(evidence, now=NOW)
        self.assertIn("systemd_coredump_storage_must_be_none", violations)
        self.assertIn("process_core_limit_must_be_zero", violations)
        self.assertIn("suid_dumping_must_be_disabled", violations)
        self.assertIn("core_dump_policy_evidence_is_stale_or_future_dated", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            core_dump_policy_violations({}, now=NOW, maximum_age_seconds=0)

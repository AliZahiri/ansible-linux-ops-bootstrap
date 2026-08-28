import unittest
from datetime import datetime, timezone

from scripts.validate_package_manager_lock import package_manager_is_ready, package_manager_lock_violations


NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


class PackageManagerLockReadinessTests(unittest.TestCase):
    def test_fresh_unlocked_hosts_pass(self):
        hosts = [{"host_id": "web-01", "observed_at": "2026-08-28T11:59:00Z", "lock_held": False}]
        self.assertTrue(package_manager_is_ready(hosts, now=NOW))

    def test_active_lock_with_owner_is_reported_without_deletion_advice(self):
        hosts = [{"host_id": "web-01", "observed_at": "2026-08-28T11:59:00Z", "lock_held": True, "owner_pid": 421, "owner_command": "unattended-upgrade", "owner_started_at": "2026-08-28T11:50:00Z"}]
        violations = package_manager_lock_violations(hosts, now=NOW)
        self.assertEqual(violations, ("host_0:package_manager_lock_is_held",))

    def test_duplicate_stale_and_incomplete_lock_evidence_fails(self):
        hosts = [{"host_id": "db-01", "observed_at": "2026-08-28T10:00:00Z", "lock_held": False}, {"host_id": "db-01", "observed_at": "naive", "lock_held": True, "owner_pid": 0, "owner_command": "", "owner_started_at": "2026-08-27T10:00:00Z"}]
        violations = package_manager_lock_violations(hosts, now=NOW)
        self.assertIn("host_1:host_id_must_be_unique", violations)
        self.assertIn("host_1:lock_owner_pid_is_required", violations)
        self.assertIn("host_1:lock_owner_exceeds_review_window", violations)

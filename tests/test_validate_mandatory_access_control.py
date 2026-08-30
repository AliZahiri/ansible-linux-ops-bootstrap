import unittest
from datetime import datetime, timezone

from scripts.validate_mandatory_access_control import mandatory_access_control_is_enforced, mandatory_access_control_violations


NOW = datetime(2026, 8, 30, 9, 0, tzinfo=timezone.utc)


class MandatoryAccessControlEvidenceTests(unittest.TestCase):
    def test_fresh_enforcing_policy_evidence_passes(self):
        hosts = [
            {"hostname": "rhel-1", "framework": "selinux", "mode": "enforcing", "policy_name": "targeted", "enforced_profile_count": 12, "denial_events_reviewed": True, "observed_at": "2026-08-30T08:30:00Z"},
            {"hostname": "ubuntu-1", "framework": "apparmor", "mode": "enforcing", "policy_name": "ubuntu-server", "enforced_profile_count": 24, "denial_events_reviewed": True, "observed_at": "2026-08-30T08:00:00+00:00"},
        ]
        self.assertTrue(mandatory_access_control_is_enforced(hosts, now=NOW))

    def test_disabled_stale_and_duplicate_host_evidence_fails(self):
        hosts = [
            {"hostname": "node-1", "framework": "none", "mode": "permissive", "policy_name": "", "enforced_profile_count": 0, "denial_events_reviewed": False, "observed_at": "2026-08-20T08:00:00Z"},
            {"hostname": "node-1", "framework": "selinux", "mode": "enforcing", "policy_name": "targeted", "enforced_profile_count": 1, "denial_events_reviewed": True, "observed_at": "2026-08-30T08:00:00Z"},
        ]
        violations = mandatory_access_control_violations(hosts, now=NOW)
        self.assertIn("host_0:framework_must_be_selinux_or_apparmor", violations)
        self.assertIn("host_0:mode_must_be_enforcing", violations)
        self.assertIn("host_0:observation_is_stale", violations)
        self.assertIn("host_1:hostname_must_be_unique", violations)

    def test_empty_hosts_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_host_is_required",), mandatory_access_control_violations([], now=NOW))
        with self.assertRaises(ValueError):
            mandatory_access_control_violations([], now=NOW, maximum_age_seconds=0)

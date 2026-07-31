import unittest
from datetime import datetime, timezone

from scripts.validate_kernel_reboot_evidence import kernel_reboot_evidence_violations, kernel_reboot_state_is_acceptable


NOW = datetime(2026, 7, 31, 10, 0, tzinfo=timezone.utc)


class KernelRebootEvidenceGateTests(unittest.TestCase):
    def test_running_latest_kernel_and_bounded_approved_deferral_pass(self):
        self.assertTrue(kernel_reboot_state_is_acceptable({"running_kernel": "6.8.0-60", "installed_kernel": "6.8.0-60"}, now=NOW))
        deferred = {"running_kernel": "6.8.0-59", "installed_kernel": "6.8.0-60", "reboot_completed": False, "deferral_ticket": "CHG-42", "deferral_deadline": "2026-07-31T18:00:00Z"}
        self.assertTrue(kernel_reboot_state_is_acceptable(deferred, now=NOW))

    def test_unapproved_excessive_or_ineffective_reboot_fails(self):
        evidence = {"running_kernel": "6.8.0-59", "installed_kernel": "6.8.0-60", "reboot_completed": False, "deferral_ticket": "", "deferral_deadline": "2026-08-02T10:00:00Z"}
        violations = kernel_reboot_evidence_violations(evidence, now=NOW)
        self.assertIn("kernel_reboot_requires_deferral_ticket", violations)
        self.assertIn("kernel_reboot_deferral_exceeds_maximum", violations)
        rebooted = {"running_kernel": "6.8.0-59", "installed_kernel": "6.8.0-60", "reboot_completed": True}
        self.assertIn("running_kernel_does_not_match_installed_after_reboot", kernel_reboot_evidence_violations(rebooted, now=NOW))

    def test_invalid_release_and_policy_fail(self):
        violations = kernel_reboot_evidence_violations({"running_kernel": "bad release", "installed_kernel": ""}, now=NOW)
        self.assertEqual(2, len(violations))
        with self.assertRaises(ValueError):
            kernel_reboot_evidence_violations({}, now=NOW, maximum_deferral_seconds=0)


if __name__ == "__main__":
    unittest.main()

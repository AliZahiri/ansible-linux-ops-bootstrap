import unittest

from scripts.validate_check_mode_change_budget import check_mode_change_budget_is_safe, check_mode_change_budget_violations


class AnsibleCheckModeChangeBudgetTests(unittest.TestCase):
    def test_healthy_bounded_check_mode_report_passes(self):
        report = {"hosts": 4, "failed": 0, "unreachable": 0, "changed": 3, "checked_at": "2026-08-23T08:00:00Z"}
        self.assertTrue(check_mode_change_budget_is_safe(report, max_changed=5))

    def test_failure_unreachable_and_excessive_change_fail(self):
        violations = check_mode_change_budget_violations({"hosts": 4, "failed": 1, "unreachable": 1, "changed": 20, "checked_at": "2026-08-23T08:00:00"}, max_changed=5)
        self.assertIn("check_mode_must_have_no_failures", violations)
        self.assertIn("check_mode_must_have_no_unreachable_hosts", violations)
        self.assertIn("changed_count_exceeds_budget", violations)

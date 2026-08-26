import unittest

from scripts.validate_host_batch_failure_budget import host_batch_failure_budget_violations, host_batch_is_within_failure_budget


class AnsibleHostBatchFailureBudgetTests(unittest.TestCase):
    def test_successful_named_batch_passes(self):
        summary = {"batch_id": "web-1", "hosts": 5, "failed": 0, "unreachable": 0, "completed_at": "2026-08-26T08:00:00Z"}
        self.assertTrue(host_batch_is_within_failure_budget(summary))

    def test_failed_and_unreachable_hosts_over_budget_fail(self):
        violations = host_batch_failure_budget_violations({"batch_id": "web-2", "hosts": 5, "failed": 1, "unreachable": 1, "completed_at": "naive"})
        self.assertIn("failed_hosts_exceed_budget", violations)
        self.assertIn("unreachable_hosts_exceed_budget", violations)
        self.assertIn("completed_at_must_be_timezone_aware", violations)

import unittest

from scripts.validate_idempotency_report import idempotency_is_proven, idempotency_violations


class IdempotencyReportGateTests(unittest.TestCase):
    def test_first_run_changes_and_zero_change_verification_pass(self):
        first = {"web-1": {"changed": 4, "failed": 0, "unreachable": 0}}
        verification = {"web-1": {"changed": 0, "failed": 0, "unreachable": 0}}

        self.assertTrue(idempotency_is_proven(first_run=first, verification_run=verification))

    def test_verification_change_and_failure_are_reported(self):
        recap = {"web-1": {"changed": 1, "failed": 1, "unreachable": 0}}

        violations = idempotency_violations(first_run=recap, verification_run=recap)

        self.assertIn("first:web-1:failed_must_be_zero", violations)
        self.assertIn("verification:web-1:changed_must_be_zero", violations)
        self.assertIn("verification:web-1:failed_must_be_zero", violations)

    def test_host_drift_and_invalid_metric_are_rejected(self):
        first = {"web-1": {"changed": 0, "failed": 0, "unreachable": 0}}
        verification = {"web-2": {"changed": False, "failed": 0, "unreachable": 0}}

        violations = idempotency_violations(first_run=first, verification_run=verification)

        self.assertIn("run_host_sets_must_match", violations)
        self.assertIn("verification:web-2:changed_must_be_a_non_negative_integer", violations)


if __name__ == "__main__":
    unittest.main()

import unittest

from scripts.validate_time_sync_health import time_sync_health_violations, time_sync_is_healthy


class TimeSyncHealthEvidenceGateTests(unittest.TestCase):
    def test_synchronized_bounded_clock_with_source_passes(self):
        evidence = {"synchronized": True, "usable_source_count": 2, "stratum": 3, "offset_ms": -12.5, "leap_status": "normal"}
        self.assertTrue(time_sync_is_healthy(evidence))

    def test_unsynchronized_source_less_invalid_and_drifted_clock_fails(self):
        evidence = {"synchronized": False, "usable_source_count": 0, "stratum": 16, "offset_ms": 250, "leap_status": "unsynchronised"}
        violations = time_sync_health_violations(evidence)
        self.assertIn("clock_must_be_synchronized", violations)
        self.assertIn("at_least_one_usable_time_source_is_required", violations)
        self.assertIn("stratum_must_be_between_1_and_15", violations)
        self.assertIn("clock_offset_exceeds_maximum", violations)
        self.assertIn("leap_status_must_be_normal", violations)

    def test_non_finite_offset_and_invalid_policy_fail(self):
        self.assertIn("clock_offset_must_be_finite", time_sync_health_violations({"offset_ms": float("nan")}))
        with self.assertRaises(ValueError):
            time_sync_health_violations({}, maximum_absolute_offset_ms=0)


if __name__ == "__main__":
    unittest.main()

import unittest

from scripts.validate_kernel_parameter_drift import kernel_parameter_drift_violations, kernel_parameters_are_converged


class LinuxKernelParameterDriftTests(unittest.TestCase):
    def test_matching_runtime_parameters_pass(self):
        evidence = {"parameters": [{"name": "net.ipv4.conf.all.accept_redirects", "expected": "0", "observed": "0"}], "reboot_required": False, "observed_at": "2026-08-23T08:00:00Z"}
        self.assertTrue(kernel_parameters_are_converged(evidence))

    def test_duplicate_drift_and_pending_reboot_fail(self):
        evidence = {"parameters": [{"name": "kernel.kptr_restrict", "expected": "2", "observed": "1"}, {"name": "kernel.kptr_restrict", "expected": "2", "observed": "2"}], "reboot_required": True, "observed_at": "naive"}
        violations = kernel_parameter_drift_violations(evidence)
        self.assertIn("parameter_0:runtime_value_drifted", violations)
        self.assertIn("parameter_1:name_must_be_unique", violations)
        self.assertIn("reboot_is_required_for_kernel_convergence", violations)

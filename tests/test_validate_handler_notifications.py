import unittest
import json
from pathlib import Path
import subprocess
import tempfile

from scripts.validate_handler_notifications import (
    handler_notification_report,
    handler_notification_violations,
    handler_notifications_are_valid,
)


class HandlerNotificationContractTests(unittest.TestCase):
    def test_defined_case_sensitive_notifications_pass(self):
        self.assertTrue(handler_notifications_are_valid(notifications=["Restart Docker", "Reload Nginx"], handlers=["Restart Docker", "Reload Nginx"]))

    def test_undefined_notifications_are_reported_deterministically(self):
        violations = handler_notification_violations(notifications=["Reload Nginx", "Restart Docker"], handlers=["Restart Docker"])
        self.assertEqual(("undefined_handler_notification:Reload Nginx",), violations)

    def test_blank_duplicate_and_case_mismatched_names_fail(self):
        violations = handler_notification_violations(notifications=["", "restart docker"], handlers=["Restart Docker", "Restart Docker", ""])
        self.assertIn("blank_handler_name_is_forbidden", violations)
        self.assertIn("blank_notification_name_is_forbidden", violations)
        self.assertIn("duplicate_handler_definition:Restart Docker", violations)
        self.assertIn("undefined_handler_notification:restart docker", violations)

    def test_non_string_names_fail_with_stable_type_violations(self):
        violations = handler_notification_violations(
            notifications=["Restart Docker", None],
            handlers=["Restart Docker", 42],
        )

        self.assertIn("handler_names_must_be_strings", violations)
        self.assertIn("notification_names_must_be_strings", violations)

    def test_report_contains_counts_and_validation_decision(self):
        report = handler_notification_report(
            notifications=["Restart Docker"],
            handlers=["Restart Docker"],
        )

        self.assertTrue(report["valid"])
        self.assertEqual(1, report["notification_count"])
        self.assertEqual([], report["violations"])

    def test_cli_returns_machine_readable_policy_result(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "handlers.json"
            input_path.write_text(
                json.dumps(
                    {
                        "notifications": ["Restart Docker", "Reload Nginx"],
                        "handlers": ["Restart Docker"],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                ["python3", "scripts/validate_handler_notifications.py", str(input_path)],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.assertEqual(1, result.returncode)
        report = json.loads(result.stdout)
        self.assertFalse(report["valid"])
        self.assertIn("undefined_handler_notification:Reload Nginx", report["violations"])

    def test_cli_rejects_missing_contract_arrays(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "handlers.json"
            input_path.write_text("{}", encoding="utf-8")
            result = subprocess.run(
                ["python3", "scripts/validate_handler_notifications.py", str(input_path)],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.assertEqual(2, result.returncode)
        self.assertIn("notifications must be a JSON array", result.stderr)


if __name__ == "__main__":
    unittest.main()

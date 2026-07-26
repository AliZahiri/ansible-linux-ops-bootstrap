import unittest

from scripts.validate_handler_notifications import handler_notification_violations, handler_notifications_are_valid


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


if __name__ == "__main__":
    unittest.main()

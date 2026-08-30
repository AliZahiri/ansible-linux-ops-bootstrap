import unittest
from datetime import datetime, timezone

from scripts.validate_sudo_command_scope import sudo_command_scope_is_safe, sudo_command_scope_violations


NOW = datetime(2026, 8, 30, 9, 0, tzinfo=timezone.utc)


class SudoCommandScopeContractTests(unittest.TestCase):
    def test_literal_scoped_command_grant_passes(self):
        grant = {"grant_id": "service-restart", "subject": "%deployers", "run_as": "root", "commands": ["/usr/bin/systemctl restart api.service", "/usr/bin/systemctl status api.service"], "passwordless": False}
        self.assertTrue(sudo_command_scope_is_safe([grant], now=NOW))

    def test_all_shell_wildcard_and_unbounded_passwordless_grants_fail(self):
        grant = {"grant_id": "unsafe", "subject": "deployer", "run_as": "root", "commands": ["ALL", "/bin/bash", "/usr/bin/systemctl restart *.service"], "passwordless": True, "approval_ticket": "", "expires_at": "2026-08-31T09:00:00Z"}
        violations = sudo_command_scope_violations([grant], now=NOW)
        self.assertEqual(3, sum(item.endswith("is_not_literal_and_scoped") for item in violations))
        self.assertIn("grant_0:passwordless_approval_ticket_is_required", violations)
        self.assertIn("grant_0:passwordless_expiry_is_outside_policy", violations)

    def test_bounded_approved_passwordless_grant_passes(self):
        grant = {"grant_id": "incident-restart", "subject": "on-call", "run_as": "root", "commands": ["/usr/bin/systemctl restart api.service"], "passwordless": True, "approval_ticket": "INC-42", "expires_at": "2026-08-30T09:30:00Z"}
        self.assertTrue(sudo_command_scope_is_safe([grant], now=NOW))

    def test_empty_grants_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_sudo_grant_is_required",), sudo_command_scope_violations([], now=NOW))
        with self.assertRaises(ValueError):
            sudo_command_scope_violations([], now=NOW, maximum_passwordless_seconds=0)

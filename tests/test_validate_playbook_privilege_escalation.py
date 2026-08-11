import unittest

from scripts.validate_playbook_privilege_escalation import playbook_privilege_escalation_is_safe, playbook_privilege_escalation_violations


class PlaybookPrivilegeEscalationGateTests(unittest.TestCase):
    def test_explicit_privilege_boundaries_pass(self):
        tasks = [{"name": "Install Docker", "become": True, "escalation_reason": "package installation"}, {"name": "Run application check", "become": False, "run_as": "deploy"}]
        self.assertTrue(playbook_privilege_escalation_is_safe(tasks))

    def test_implicit_duplicate_and_unjustified_escalation_fails(self):
        tasks = [{"name": "Install Docker", "become": True}, {"name": "Install Docker", "become": False, "run_as": "root"}, {"name": "Unknown"}]
        violations = playbook_privilege_escalation_violations(tasks)
        self.assertIn("task_0:privileged_task_requires_reason", violations)
        self.assertIn("task_1:name_must_be_unique", violations)
        self.assertIn("task_1:non_privileged_task_requires_non_root_user", violations)
        self.assertIn("task_2:become_must_be_explicit_boolean", violations)


if __name__ == "__main__":
    unittest.main()

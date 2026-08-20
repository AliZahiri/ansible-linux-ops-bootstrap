import unittest

from scripts.validate_playbook_change_control import playbook_change_control_is_valid, playbook_change_control_violations


class PlaybookChangeControlGateTests(unittest.TestCase):
    def test_tagged_risky_task_with_recovery_evidence_passes(self):
        tasks = [{"name": "Apply kernel setting", "tags": ["hardening"], "module": "ansible.builtin.command", "change_ticket": "OPS-44", "rollback_plan": "restore previous sysctl value"}]
        self.assertTrue(playbook_change_control_is_valid(tasks))

    def test_untagged_risky_task_without_change_evidence_fails(self):
        violations = playbook_change_control_violations([{"name": "", "tags": [], "module": "ansible.builtin.reboot"}])
        self.assertEqual(violations, ("task_0:name_is_required", "task_0:explicit_tags_are_required", "task_0:change_ticket_is_required_for_risky_module", "task_0:rollback_plan_is_required_for_risky_module"))

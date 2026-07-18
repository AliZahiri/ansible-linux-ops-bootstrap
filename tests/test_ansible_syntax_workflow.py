import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AnsibleSyntaxWorkflowTests(unittest.TestCase):
    def test_validation_workflow_checks_all_playbooks_with_sample_inventory(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

        self.assertIn('ansible-core>=2.18,<2.19', workflow)
        self.assertIn("ansible-galaxy collection install -r requirements.yml", workflow)
        self.assertIn("ansible-playbook --syntax-check -i inventories/sample/hosts.ini", workflow)
        for playbook in ("playbooks/bootstrap.yml", "playbooks/monitoring.yml", "playbooks/backup.yml"):
            self.assertIn(playbook, workflow)

    def test_validation_workflow_does_not_reference_production_inventory(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

        self.assertNotIn("inventories/production", workflow)


if __name__ == "__main__":
    unittest.main()

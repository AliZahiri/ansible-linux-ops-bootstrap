import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / 'scripts/validate_playbook_roles.py'
SPEC = importlib.util.spec_from_file_location('validate_playbook_roles', SCRIPT_PATH)
validate_playbook_roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_playbook_roles)


class PlaybookRoleContractTests(unittest.TestCase):
    def test_existing_role_entrypoints_are_valid(self):
        self.assertTrue(
            validate_playbook_roles.role_contract_is_valid(
                ROOT, ('common', 'firewall', 'docker', 'node_exporter', 'backup')
            )
        )

    def test_missing_role_entrypoint_is_reported(self):
        self.assertEqual(
            validate_playbook_roles.missing_role_entrypoints(ROOT, ('common', 'missing-role')),
            ('missing-role',),
        )


if __name__ == '__main__':
    unittest.main()

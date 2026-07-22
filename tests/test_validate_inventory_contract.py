import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_inventory_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_inventory_contract", SCRIPT_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class InventoryContractTests(unittest.TestCase):
    def test_grouped_hosts_without_secrets_pass(self):
        self.assertTrue(validator.inventory_contract_is_valid("[web]\nweb-1 ansible_host=192.0.2.10\n"))

    def test_duplicate_alias_is_reported(self):
        violations = validator.inventory_contract_violations("[web]\nnode-1\n[workers]\nnode-1\n")
        self.assertIn("line_4:duplicate_host_alias:node-1", violations)

    def test_inline_credentials_are_rejected(self):
        violations = validator.inventory_contract_violations("[web]\nweb-1 ansible_password=secret\n")
        self.assertIn("line_2:inline_sensitive_inventory_variable_is_forbidden", violations)

    def test_empty_inventory_fails(self):
        self.assertEqual(("inventory_requires_at_least_one_grouped_host",), validator.inventory_contract_violations("# empty"))


if __name__ == "__main__":
    unittest.main()

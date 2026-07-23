import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_vault_references.py"
SPEC = importlib.util.spec_from_file_location("validate_vault_references", SCRIPT_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class VaultReferenceTests(unittest.TestCase):
    def test_vault_reference_and_non_secret_values_pass(self):
        variables = {"database_password": "{{ vault_database_password }}", "service_port": 5432}
        self.assertTrue(validator.vault_references_are_valid(variables))

    def test_plaintext_secret_names_are_reported_without_values(self):
        variables = {"api_token": "do-not-log", "database_password": "plaintext"}
        self.assertEqual(("api_token", "database_password"), validator.plaintext_secret_variable_names(variables))

    def test_empty_prefix_is_rejected(self):
        with self.assertRaises(ValueError):
            validator.vault_references_are_valid({}, vault_prefix="")


if __name__ == "__main__":
    unittest.main()

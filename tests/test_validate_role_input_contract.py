import unittest

from scripts.validate_role_input_contract import role_input_contract_is_valid


class RoleInputContractTests(unittest.TestCase):
    def test_required_role_values_pass_when_declared(self):
        self.assertTrue(role_input_contract_is_valid({"backup_user": "backup"}, ("backup_user",)))

    def test_blank_required_role_value_fails(self):
        self.assertFalse(role_input_contract_is_valid({"backup_user": ""}, ("backup_user",)))

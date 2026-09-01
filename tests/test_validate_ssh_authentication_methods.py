import unittest

from scripts.validate_ssh_authentication_methods import ssh_authentication_is_hardened, ssh_authentication_violations


class SSHAuthenticationMethodContractTests(unittest.TestCase):
    def test_public_key_only_configuration_passes(self):
        config = {"pubkey_authentication": True, "password_authentication": False, "kbd_interactive_authentication": False, "permit_root_login": "no", "authentication_methods": "publickey"}
        self.assertTrue(ssh_authentication_is_hardened(config))

    def test_password_keyboard_interactive_and_root_login_fail(self):
        config = {"pubkey_authentication": True, "password_authentication": True, "kbd_interactive_authentication": True, "permit_root_login": "prohibit-password", "authentication_methods": "publickey,password"}
        violations = ssh_authentication_violations(config)
        self.assertIn("password_authentication_must_be_disabled", violations)
        self.assertIn("keyboard_interactive_authentication_must_be_disabled", violations)
        self.assertIn("direct_root_login_must_be_disabled", violations)
        self.assertIn("authentication_methods_must_use_public_key_only", violations)

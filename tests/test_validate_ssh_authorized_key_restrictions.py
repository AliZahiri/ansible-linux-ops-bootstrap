import unittest
from scripts.validate_ssh_authorized_key_restrictions import ssh_authorized_key_restriction_violations
class SshAuthorizedKeyRestrictionTests(unittest.TestCase):
    def test_restricted_automation_key_passes(self):
        entry={'allow_agent_forwarding':False,'allow_port_forwarding':False,'interactive_access':False,'forced_command':'/usr/local/bin/backup','allow_pty':False}
        self.assertEqual((), ssh_authorized_key_restriction_violations([entry]))
    def test_broad_key_fails(self):
        violations=ssh_authorized_key_restriction_violations([{'allow_agent_forwarding':True,'allow_port_forwarding':True,'interactive_access':False,'allow_pty':True}])
        self.assertIn('entry_0:agent_forwarding_must_be_disabled', violations); self.assertIn('entry_0:non_interactive_key_requires_forced_command', violations); self.assertIn('entry_0:non_interactive_key_must_disable_pty', violations)

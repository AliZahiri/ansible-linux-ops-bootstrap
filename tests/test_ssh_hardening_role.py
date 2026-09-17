import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SshHardeningRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.variables = (ROOT / "group_vars/all.yml").read_text(encoding="utf-8")
        cls.tasks = (ROOT / "roles/common/tasks/main.yml").read_text(encoding="utf-8")
        cls.handlers = (ROOT / "roles/common/handlers/main.yml").read_text(
            encoding="utf-8"
        )

    def test_hardening_is_opt_in_and_keeps_password_authentication_disabled(self):
        self.assertIn("ssh_hardening_enabled: false", self.variables)
        self.assertIn('ssh_password_authentication: "no"', self.variables)
        self.assertIn("when: ssh_hardening_enabled | bool", self.tasks)

    def test_role_refuses_to_harden_without_operations_user_access(self):
        self.assertIn("ops_user in ssh_allowed_users", self.tasks)
        self.assertIn("ansible.builtin.stat:", self.tasks)
        self.assertIn("ssh_authorized_keys_path", self.tasks)
        self.assertIn("ops_authorized_keys.stat.exists", self.tasks)
        self.assertIn("ops_authorized_keys.stat.size", self.tasks)
        self.assertIn("Verify sshd loads the managed drop-in directory", self.tasks)
        self.assertIn("/etc/ssh/sshd_config.d/", self.tasks)

    def test_drop_ins_are_validated_before_reload(self):
        self.assertIn('validate: "/usr/sbin/sshd -t -f %s"', self.tasks)
        self.assertIn("notify: Validate and reload SSH", self.tasks)
        self.assertIn("ansible.builtin.command: /usr/sbin/sshd -t", self.handlers)
        self.assertLess(
            self.handlers.index("ansible.builtin.command: /usr/sbin/sshd -t"),
            self.handlers.index("ansible.builtin.service:"),
        )
        self.assertIn('name: "{{ ssh_service_name }}"', self.handlers)
        self.assertIn("state: reloaded", self.handlers)


if __name__ == "__main__":
    unittest.main()

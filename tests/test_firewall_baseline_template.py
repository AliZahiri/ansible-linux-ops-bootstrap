import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FirewallBaselineTemplateTests(unittest.TestCase):
    def test_firewall_template_declares_ssh_and_app_ports(self):
        content = (ROOT / "roles/firewall/templates/ufw-baseline.rules.j2").read_text(encoding="utf-8")

        self.assertIn("default deny incoming", content)
        self.assertIn("trusted_ssh_cidr", content)
        self.assertIn("app_tcp_ports", content)

    def test_firewall_template_sorts_unique_lists_and_supports_private_cidrs(self):
        content = (ROOT / "roles/firewall/templates/ufw-baseline.rules.j2").read_text(encoding="utf-8")

        self.assertIn("| unique | sort", content)
        self.assertIn("trusted_app_cidrs", content)
        self.assertIn("app_private_port", content)


if __name__ == "__main__":
    unittest.main()

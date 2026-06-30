import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SysctlHardeningTemplateTests(unittest.TestCase):
    def test_sysctl_template_has_network_hardening_defaults(self):
        content = (ROOT / "roles/common/templates/99-hardening.conf.j2").read_text(encoding="utf-8")

        self.assertIn("net.ipv4.ip_forward = 0", content)
        self.assertIn("rp_filter = 1", content)
        self.assertIn("accept_redirects = 0", content)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MotdOpsBannerTemplateTests(unittest.TestCase):
    def test_banner_template_has_owner_and_secret_warning(self):
        content = (ROOT / "roles/common/templates/motd-ops-banner.j2").read_text(encoding="utf-8")

        self.assertIn("environment_name", content)
        self.assertIn("platform_owner", content)
        self.assertIn("Do not paste secrets", content)


if __name__ == "__main__":
    unittest.main()

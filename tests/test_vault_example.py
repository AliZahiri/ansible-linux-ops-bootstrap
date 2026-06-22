import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VaultExampleTests(unittest.TestCase):
    def test_vault_example_uses_placeholders_only(self):
        example = ROOT / "group_vars/vault.example.yml"
        content = example.read_text(encoding="utf-8")

        self.assertIn("CHANGE_ME_WITH_ANSIBLE_VAULT", content)
        self.assertNotIn("password123", content.lower())


if __name__ == "__main__":
    unittest.main()

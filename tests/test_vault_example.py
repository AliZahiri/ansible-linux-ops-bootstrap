import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VaultExampleTests(unittest.TestCase):
    def test_vault_example_uses_placeholders_only(self):
        example = ROOT / "group_vars/vault.example.yml"
        content = example.read_text(encoding="utf-8")

        self.assertIn("CHANGE_ME_WITH_ANSIBLE_VAULT", content)
        self.assertNotIn("password123", content.lower())

    def test_vault_example_keeps_secret_names_explicit(self):
        example = ROOT / "group_vars/vault.example.yml"
        keys = [
            line.split(":", 1)[0]
            for line in example.read_text(encoding="utf-8").splitlines()
            if line and not line.startswith("#")
        ]

        self.assertTrue(keys)
        self.assertTrue(all(key.startswith("vault_") for key in keys))


if __name__ == "__main__":
    unittest.main()

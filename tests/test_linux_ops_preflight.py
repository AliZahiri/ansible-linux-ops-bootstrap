import tempfile
import unittest
from pathlib import Path

from scripts.linux_ops_preflight import linux_ops_preflight, linux_ops_preflight_is_ready


class LinuxOpsPreflightTests(unittest.TestCase):
    def test_valid_inventory_vault_reference_and_role_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "roles/common/tasks").mkdir(parents=True)
            (root / "roles/common/tasks/main.yml").write_text("---\n", encoding="utf-8")
            self.assertTrue(linux_ops_preflight_is_ready(root=root, inventory_content="[web]\nweb-1\n", variables={"database_password": "{{ vault_database_password }}"}, role_names=["common"]))

    def test_failures_are_partitioned_without_secret_values(self):
        report = linux_ops_preflight(root=Path("/missing"), inventory_content="# empty", variables={"api_token": "do-not-return"}, role_names=["missing"] )
        self.assertIn("inventory_requires_at_least_one_grouped_host", report["inventory"])
        self.assertEqual(("api_token",), report["vault_references"])
        self.assertEqual(("missing",), report["role_entrypoints"])
        self.assertNotIn("do-not-return", repr(report))


if __name__ == "__main__":
    unittest.main()

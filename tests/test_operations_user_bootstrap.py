import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OperationsUserBootstrapTests(unittest.TestCase):
    def test_common_role_does_not_require_docker_group_before_install(self):
        variables = (ROOT / "group_vars/all.yml").read_text(encoding="utf-8")
        ops_groups = variables.split("ops_groups:", 1)[1].split("base_packages:", 1)[0]

        self.assertIn("- sudo", ops_groups)
        self.assertNotIn("- docker", ops_groups)

    def test_docker_role_adds_operations_user_after_package_install(self):
        tasks = (ROOT / "roles/docker/tasks/main.yml").read_text(encoding="utf-8")

        self.assertLess(
            tasks.index("name: Install Docker packages"),
            tasks.index("name: Add operations user to docker group"),
        )
        self.assertIn("- docker", tasks)
        self.assertIn("append: true", tasks)


if __name__ == "__main__":
    unittest.main()

import unittest

from scripts.validate_role_dependency_graph import role_dependency_graph_is_valid, role_dependency_graph_violations


class RoleDependencyGraphGateTests(unittest.TestCase):
    def test_declared_acyclic_role_dependencies_pass(self):
        roles = [{"name": "common", "dependencies": []}, {"name": "docker", "dependencies": ["common"]}, {"name": "monitoring", "dependencies": ["common", "docker"]}]
        self.assertTrue(role_dependency_graph_is_valid(roles))

    def test_missing_self_duplicate_and_cyclic_dependencies_fail(self):
        roles = [{"name": "common", "dependencies": ["common", "missing"]}, {"name": "docker", "dependencies": ["monitoring"]}, {"name": "monitoring", "dependencies": ["docker"]}, {"name": "docker", "dependencies": []}]
        violations = role_dependency_graph_violations(roles)
        self.assertIn("role:common:cannot_depend_on_itself", violations)
        self.assertIn("role:common:dependency:missing:is_not_declared", violations)
        self.assertIn("role_3:name_must_be_unique", violations)
        self.assertIn("role_dependency_cycle_detected", violations)

    def test_empty_role_set_fails(self):
        self.assertEqual(("at_least_one_role_is_required",), role_dependency_graph_violations([]))


if __name__ == "__main__":
    unittest.main()

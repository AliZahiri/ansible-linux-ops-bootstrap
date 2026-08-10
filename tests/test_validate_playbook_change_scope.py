import unittest

from scripts.validate_playbook_change_scope import playbook_change_scope_is_safe, playbook_change_scope_violations


class PlaybookChangeScopeGateTests(unittest.TestCase):
    def test_reviewable_non_destructive_scope_passes(self):
        evidence = {"inventory": "inventories/staging.ini", "host_count": 3, "tags": ["docker"], "has_destructive_changes": False}

        self.assertTrue(playbook_change_scope_is_safe(evidence))

    def test_default_inventory_unbounded_scope_and_unacknowledged_change_fail(self):
        evidence = {"inventory": "production.ini", "host_count": 101, "tags": [], "has_destructive_changes": True, "operator_acknowledged": False}

        violations = playbook_change_scope_violations(evidence)

        self.assertIn("inventory_must_be_an_explicit_non_default_name", violations)
        self.assertIn("host_count_must_be_within_review_limit", violations)
        self.assertIn("tags_must_be_a_non_empty_string_list", violations)
        self.assertIn("destructive_changes_require_operator_acknowledgement", violations)

    def test_invalid_host_limit_fails(self):
        with self.assertRaises(ValueError):
            playbook_change_scope_violations({}, maximum_hosts=0)


if __name__ == "__main__":
    unittest.main()

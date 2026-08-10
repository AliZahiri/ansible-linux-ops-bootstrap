import unittest

from scripts.validate_collection_version_lock import collection_version_lock_is_safe, collection_version_lock_violations


class CollectionVersionLockGateTests(unittest.TestCase):
    def test_unique_exact_collection_locks_pass(self):
        collections = [{"name": "community.general", "version": "=10.0.0", "source": "https://galaxy.ansible.com"}]

        self.assertTrue(collection_version_lock_is_safe(collections))

    def test_duplicate_floating_and_untrusted_locks_fail(self):
        collections = [{"name": "community.general", "version": ">=10.0", "source": "http://example.test"}, {"name": "Community.General", "version": "=10.0.0", "source": "https://galaxy.ansible.com"}]

        violations = collection_version_lock_violations(collections)

        self.assertIn("collection_0:version_must_be_exact_semver_pin", violations)
        self.assertIn("collection_0:source_must_be_https", violations)
        self.assertIn("collection_1:name_must_be_unique", violations)

    def test_empty_collection_set_fails(self):
        self.assertEqual(("at_least_one_collection_lock_is_required",), collection_version_lock_violations([]))


if __name__ == "__main__":
    unittest.main()

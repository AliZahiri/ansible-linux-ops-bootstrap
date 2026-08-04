import unittest

from scripts.validate_filesystem_capacity import filesystem_capacity_violations


class FilesystemCapacityInodeEvidenceGateTests(unittest.TestCase):
    def test_writable_filesystems_below_byte_and_inode_limits_pass(self):
        filesystems = [{"mount": "/", "writable": True, "used_percent": 60, "inode_used_percent": 40}, {"mount": "/var", "writable": True, "used_percent": 70, "inode_used_percent": 50}]
        self.assertEqual((), filesystem_capacity_violations(filesystems))

    def test_relative_readonly_and_exhausted_filesystem_fails(self):
        filesystems = [{"mount": "var", "writable": False, "used_percent": 90, "inode_used_percent": 101}]
        violations = filesystem_capacity_violations(filesystems)
        self.assertIn("filesystem_0:mount_must_be_absolute", violations)
        self.assertIn("filesystem_0:mount_must_be_writable", violations)
        self.assertIn("filesystem_0:used_percent_exceeds_maximum", violations)
        self.assertIn("filesystem_0:inode_used_percent_must_be_between_zero_and_100", violations)

    def test_empty_input_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_one_filesystem_observation_is_required",), filesystem_capacity_violations([]))
        with self.assertRaises(ValueError):
            filesystem_capacity_violations([], maximum_used_percent=100)


if __name__ == "__main__":
    unittest.main()

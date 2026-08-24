import unittest

from scripts.validate_filesystem_mount_safety import filesystem_mount_safety_violations, filesystem_mounts_are_safe


class LinuxFilesystemMountSafetyTests(unittest.TestCase):
    def test_root_and_hardened_temporary_mount_pass(self):
        mounts = [{"target": "/", "fstype": "ext4", "options": ["defaults"]}, {"target": "/tmp", "fstype": "tmpfs", "options": ["nodev", "nosuid", "noexec"]}]
        self.assertTrue(filesystem_mounts_are_safe(mounts, {"/tmp": {"nodev", "nosuid", "noexec"}}))

    def test_duplicate_relative_and_under_hardened_mounts_fail(self):
        mounts = [{"target": "tmp", "fstype": "", "options": []}, {"target": "/tmp", "fstype": "tmpfs", "options": ["nodev"]}, {"target": "/tmp", "fstype": "tmpfs", "options": ["nodev"]}]
        violations = filesystem_mount_safety_violations(mounts, {"/tmp": {"nodev", "nosuid"}})
        self.assertIn("mount_2:target_must_be_unique", violations)
        self.assertIn("mount_1:required_option_nosuid_is_missing", violations)
        self.assertIn("root_mount_is_required", violations)

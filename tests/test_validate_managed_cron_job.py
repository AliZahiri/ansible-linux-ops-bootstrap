import unittest

from scripts.validate_managed_cron_job import managed_cron_job_is_safe, managed_cron_job_violations


class ManagedCronJobContractGateTests(unittest.TestCase):
    def test_owned_bounded_observable_job_passes(self):
        jobs = [{"name": "backup", "schedule": "0 2 * * *", "owner": "backup", "log_path": "/var/log/backup.log"}]
        self.assertTrue(managed_cron_job_is_safe(jobs))

    def test_duplicate_unbounded_root_and_unsafe_job_fails(self):
        jobs = [{"name": "backup", "schedule": "* * * * *", "owner": "root", "log_path": "/tmp/backup.log"}, {"name": "backup", "schedule": "0 2 * * *", "owner": "backup", "log_path": "/var/log/backup.log"}]
        violations = managed_cron_job_violations(jobs)
        self.assertIn("job_0:schedule_must_be_bounded_five_field_cron", violations)
        self.assertIn("job_0:owner_must_be_explicit_non_root", violations)
        self.assertIn("job_0:log_path_must_be_under_var_log", violations)
        self.assertIn("job_1:name_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()

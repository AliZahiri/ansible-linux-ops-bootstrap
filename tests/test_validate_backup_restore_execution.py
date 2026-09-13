import unittest
from datetime import datetime, timezone
from scripts.validate_backup_restore_execution import backup_restore_execution_violations
NOW=datetime(2026,9,13,12,tzinfo=timezone.utc)
class BackupRestoreExecutionTests(unittest.TestCase):
    def test_fresh_isolated_restore_passes(self):
        e={'recovery_point_id':'rp-7','restore_succeeded':True,'isolated_destination':True,'restored_sha256':'sha256:'+'a'*64,'observed_at':'2026-09-12T12:00:00Z'}
        self.assertEqual((),backup_restore_execution_violations(e,recovery_point_id='rp-7',now=NOW))
    def test_wrong_failed_unisolated_and_stale_restore_fails(self):
        e={'recovery_point_id':'old','restore_succeeded':False,'isolated_destination':False,'restored_sha256':'bad','observed_at':'2026-07-01T00:00:00Z'}
        v=backup_restore_execution_violations(e,recovery_point_id='rp-7',now=NOW)
        self.assertIn('restore_must_succeed',v); self.assertIn('restore_destination_must_be_isolated',v); self.assertIn('restore_evidence_is_invalid_stale_or_future_dated',v)
    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError): backup_restore_execution_violations({},recovery_point_id='',now=NOW)

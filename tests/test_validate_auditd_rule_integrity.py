import unittest
from datetime import datetime, timezone

from scripts.validate_auditd_rule_integrity import auditd_rule_integrity_is_verified, auditd_rule_integrity_violations


NOW = datetime(2026, 9, 3, 6, 0, tzinfo=timezone.utc)


class AuditdRuleIntegrityEvidenceTests(unittest.TestCase):
    def test_fresh_loaded_immutable_rules_pass(self):
        evidence = {"service_active": True, "rules_loaded": True, "loaded_rule_count": 24, "rules_sha256": "sha256:" + "a" * 64, "rules_immutable": True, "observed_at": "2026-09-03T05:55:00Z"}
        self.assertTrue(auditd_rule_integrity_is_verified(evidence, now=NOW, require_immutable_rules=True))

    def test_inactive_unloaded_mutable_and_stale_evidence_fail(self):
        evidence = {"service_active": False, "rules_loaded": False, "loaded_rule_count": 0, "rules_sha256": "bad", "rules_immutable": False, "observed_at": "2026-09-03T04:00:00Z"}
        violations = auditd_rule_integrity_violations(evidence, now=NOW, require_immutable_rules=True)
        self.assertIn("auditd_service_must_be_active", violations)
        self.assertIn("auditd_rules_must_be_loaded", violations)
        self.assertIn("rules_sha256_must_be_a_sha256_digest", violations)
        self.assertIn("auditd_rules_must_be_immutable", violations)
        self.assertIn("auditd_rule_evidence_is_stale_or_future_dated", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            auditd_rule_integrity_violations({}, now=NOW, maximum_age_seconds=0)

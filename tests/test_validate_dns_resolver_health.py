import unittest
from datetime import datetime, timezone

from scripts.validate_dns_resolver_health import dns_resolver_health_violations, dns_resolvers_are_healthy


NOW = datetime(2026, 8, 29, 12, 0, tzinfo=timezone.utc)


class DnsResolverHealthEvidenceTests(unittest.TestCase):
    def test_fresh_redundant_successful_resolver_evidence_passes(self):
        hosts = [{"host_id": "web-01", "nameservers": ["10.0.0.2", "10.0.0.3"], "observed_at": "2026-08-29T11:59:00Z", "lookup_succeeded": True, "resolution_latency_ms": 12.5}]
        self.assertTrue(dns_resolvers_are_healthy(hosts, now=NOW))

    def test_duplicate_single_stale_slow_resolver_evidence_fails(self):
        hosts = [{"host_id": "web-01", "nameservers": ["10.0.0.2"], "observed_at": "2026-08-29T10:00:00Z", "lookup_succeeded": False, "resolution_latency_ms": 2500}]
        violations = dns_resolver_health_violations(hosts, now=NOW)
        self.assertIn("host_0:nameserver_coverage_is_below_minimum", violations)
        self.assertIn("host_0:observation_is_stale_or_invalid", violations)
        self.assertIn("host_0:dns_lookup_must_succeed", violations)
        self.assertIn("host_0:resolution_latency_exceeds_budget", violations)

    def test_invalid_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            dns_resolver_health_violations([], now=NOW, minimum_nameservers=0)

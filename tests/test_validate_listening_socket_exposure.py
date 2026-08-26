import unittest

from scripts.validate_listening_socket_exposure import (
    listening_socket_exposure_is_safe,
    listening_socket_exposure_violations,
)


class ListeningSocketExposureEvidenceGateTests(unittest.TestCase):
    def test_loopback_database_and_allowlisted_ssh_pass(self):
        evidence = {
            "observed_at": "2026-08-26T08:00:00Z",
            "sockets": [
                {"protocol": "tcp", "address": "127.0.0.1", "port": 5432, "process": "postgres"},
                {"protocol": "tcp", "address": "0.0.0.0", "port": 22, "process": "sshd"},
            ],
        }

        self.assertTrue(listening_socket_exposure_is_safe(evidence, allowed_public_ports={22}))

    def test_unapproved_duplicate_and_naive_evidence_fail(self):
        listener = {"protocol": "tcp", "address": "0.0.0.0", "port": 9100, "process": "node_exporter"}
        evidence = {"observed_at": "2026-08-26T08:00:00", "sockets": [listener, dict(listener)]}
        violations = listening_socket_exposure_violations(evidence, allowed_public_ports={22})

        self.assertIn("socket_0:public_port_9100_is_not_allowed", violations)
        self.assertIn("socket_1:listener_must_be_unique", violations)
        self.assertIn("observed_at_must_be_timezone_aware", violations)

    def test_invalid_allowlist_is_rejected(self):
        with self.assertRaises(ValueError):
            listening_socket_exposure_violations({}, allowed_public_ports={0})


if __name__ == "__main__":
    unittest.main()

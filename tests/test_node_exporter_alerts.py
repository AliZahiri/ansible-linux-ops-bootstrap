import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class NodeExporterAlertsTests(unittest.TestCase):
    def test_alert_template_contains_disk_and_memory_alerts(self):
        template = ROOT / "roles/node_exporter/templates/node-exporter-alerts.yml.j2"
        content = template.read_text(encoding="utf-8")

        self.assertIn("HostDiskSpaceLow", content)
        self.assertIn("HostMemoryPressure", content)
        self.assertIn("node_filesystem_avail_bytes", content)


if __name__ == "__main__":
    unittest.main()

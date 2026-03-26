from __future__ import annotations

import unittest

from qrc_ising_core.mcp_adapter import (
    list_baselines,
    package_metadata,
    simulate_one,
    symbolic_report,
)


class TestMCPAdapter(unittest.TestCase):
    def test_baselines_exposed(self) -> None:
        baselines = list_baselines()
        self.assertGreaterEqual(len(baselines), 2)
        self.assertEqual(sorted(baselines), baselines)

    def test_simulate_one_returns_metrics_payload(self) -> None:
        payload = simulate_one(
            {
                "tier": "D_mid",
                "eta": 0.005,
                "shots": 512,
                "observable_budget": 16,
                "seed": 11,
            }
        )
        self.assertIn("accuracy", payload)
        self.assertIn("error_rate", payload)
        self.assertGreaterEqual(payload["accuracy"], 0.05)

    def test_symbolic_report_returns_bool_map(self) -> None:
        checks = symbolic_report()
        self.assertIn("fc1_gap_error_equivalence", checks)
        self.assertTrue(all(isinstance(v, bool) for v in checks.values()))

    def test_package_metadata_fields(self) -> None:
        metadata = package_metadata()
        self.assertEqual(metadata["package"], "qrc-ising-core")
        self.assertEqual(metadata["import_name"], "qrc_ising_core")


if __name__ == "__main__":
    unittest.main()

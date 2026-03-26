from __future__ import annotations

import unittest

import numpy as np

from qrc_ising_core import (
    BASELINE_ACCURACY,
    QRCScenario,
    bootstrap_ci,
    simulate_accuracy,
    simulate_metrics,
)


class TestCore(unittest.TestCase):
    def test_accuracy_bounds(self) -> None:
        scenario = QRCScenario(
            tier="D_mid",
            baseline="QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout",
            eta=0.005,
            shots=512,
            observable_budget=16,
            seed=11,
        )
        acc = simulate_accuracy(scenario)
        self.assertGreaterEqual(acc, 0.05)
        self.assertLessEqual(acc, 0.995)

    def test_metrics_have_expected_fields(self) -> None:
        scenario = QRCScenario(
            tier="D_hard",
            baseline="Classical echo-state network (ESN) with matched state dimension and linear ridge readout",
            eta=0.01,
            shots=128,
            observable_budget=8,
            seed=7,
        )
        metrics = simulate_metrics(scenario)
        self.assertEqual(metrics.error_rate, 1.0 - metrics.accuracy)
        self.assertLessEqual(metrics.macro_f1, metrics.accuracy)

    def test_bootstrap_ci_ordering(self) -> None:
        values = np.array([0.74, 0.75, 0.77, 0.79, 0.80], dtype=float)
        lo, hi = bootstrap_ci(values, n_boot=200, alpha=0.1, seed=5)
        self.assertLessEqual(lo, hi)

    def test_baseline_catalog_not_empty(self) -> None:
        self.assertGreaterEqual(len(BASELINE_ACCURACY), 2)


if __name__ == "__main__":
    unittest.main()

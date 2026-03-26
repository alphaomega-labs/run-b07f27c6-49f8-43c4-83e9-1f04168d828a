from __future__ import annotations

import unittest

from qrc_ising_core import run_symbolic_checks


class TestSymbolic(unittest.TestCase):
    def test_symbolic_checks_expected_keys(self) -> None:
        result = run_symbolic_checks()
        expected = {
            "fc1_gap_error_equivalence",
            "fc1_robust_min_lower_bound",
            "fc2_loss_accuracy_equivalence",
            "fc3_ratio_dominance_equivalence",
            "fc3_undefined_ratio_guard",
        }
        self.assertEqual(set(result.keys()), expected)
        self.assertTrue(all(isinstance(value, bool) for value in result.values()))


if __name__ == "__main__":
    unittest.main()

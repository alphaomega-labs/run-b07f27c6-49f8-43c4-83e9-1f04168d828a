from __future__ import annotations

from qrc_validation.simulate import SimCell, make_row, simulate_accuracy


def test_accuracy_bounds() -> None:
    acc = simulate_accuracy(
        SimCell(
            tier="D_mid",
            baseline="QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout",
            eta=0.005,
            shots=512,
            observable_budget=16,
            seed=11,
        )
    )
    assert 0.05 <= acc <= 0.995


def test_row_has_expected_metrics() -> None:
    row = make_row(
        SimCell(
            tier="D_hard",
            baseline="Classical echo-state network (ESN) with matched state dimension and linear ridge readout",
            eta=0.01,
            shots=128,
            observable_budget=8,
            seed=7,
        )
    )
    for key in ["accuracy", "error_rate", "macro_f1", "expected_calibration_error"]:
        assert key in row

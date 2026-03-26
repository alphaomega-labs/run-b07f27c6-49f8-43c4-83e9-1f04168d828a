from qrc_ising_core import QRCScenario, run_symbolic_checks, simulate_accuracy


def main() -> None:
    scenario = QRCScenario(
        tier="D_mid",
        baseline="QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout",
        eta=0.005,
        shots=512,
        observable_budget=16,
        seed=11,
    )
    accuracy = simulate_accuracy(scenario)
    checks = run_symbolic_checks()
    print(f"simulated_accuracy={accuracy:.4f}")
    print(f"fc1_gap_error_equivalence={checks['fc1_gap_error_equivalence']}")


if __name__ == "__main__":
    main()

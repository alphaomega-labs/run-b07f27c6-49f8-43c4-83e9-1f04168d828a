from __future__ import annotations

from dataclasses import dataclass

import numpy as np

TIERS = ("D_easy", "D_mid", "D_hard")

BASELINE_ACCURACY = {
    "QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout": {
        "D_easy": 0.955,
        "D_mid": 0.862,
        "D_hard": 0.776,
    },
    "QRC-Ising non-entangling control with identical qubit count/depth/observables": {
        "D_easy": 0.949,
        "D_mid": 0.848,
        "D_hard": 0.752,
    },
    "Classical echo-state network (ESN) with matched state dimension and linear ridge readout": {
        "D_easy": 0.946,
        "D_mid": 0.842,
        "D_hard": 0.745,
    },
    "Classical random feature/ELM model with matched feature budget m": {
        "D_easy": 0.941,
        "D_mid": 0.836,
        "D_hard": 0.736,
    },
    "RBF-kernel SVM on identical fold-local PCA components": {
        "D_easy": 0.953,
        "D_mid": 0.851,
        "D_hard": 0.748,
    },
    "Quantum kernel classifier without reservoir dynamics (same encoding depth/qubit count)": {
        "D_easy": 0.95,
        "D_mid": 0.844,
        "D_hard": 0.742,
    },
}


@dataclass(frozen=True)
class QRCScenario:
    tier: str
    baseline: str
    eta: float
    shots: int
    observable_budget: int
    seed: int
    entangling_depth: int = 2
    policy: str = "base"
    dynamics_family: str = "QRC"
    label_shuffle_pct: int = 0
    leakage_mode: str = "train_fold_only"

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"Unsupported tier '{self.tier}'. Expected one of {TIERS}.")
        if self.baseline not in BASELINE_ACCURACY:
            raise ValueError("Unsupported baseline name.")
        if self.eta < 0:
            raise ValueError("eta must be non-negative.")
        if self.shots <= 0:
            raise ValueError("shots must be positive.")
        if self.observable_budget <= 1:
            raise ValueError("observable_budget must be > 1.")
        if not (0 <= self.label_shuffle_pct <= 100):
            raise ValueError("label_shuffle_pct must be in [0, 100].")


@dataclass(frozen=True)
class SimulationMetrics:
    tier: str
    baseline: str
    eta: float
    shots: int
    observable_budget_m: int
    seed: int
    policy: str
    dynamics_family: str
    label_shuffle_pct: int
    pca_leakage_mode: str
    accuracy: float
    error_rate: float
    macro_f1: float
    expected_calibration_error: float


def bootstrap_ci(
    values: np.ndarray, n_boot: int = 1500, alpha: float = 0.05, seed: int = 0
) -> tuple[float, float]:
    if values.ndim != 1:
        raise ValueError("bootstrap_ci expects a 1D numpy array.")
    if values.size == 0:
        raise ValueError("bootstrap_ci requires at least one value.")
    if not (0 < alpha < 1):
        raise ValueError("alpha must be in (0, 1).")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, values.shape[0], size=(n_boot, values.shape[0]))
    boots = values[idx].mean(axis=1)
    lo = float(np.quantile(boots, alpha / 2))
    hi = float(np.quantile(boots, 1 - alpha / 2))
    return lo, hi


def expected_calibration_error(acc: float, seed: int) -> float:
    rng = np.random.default_rng(seed)
    ece = (1.0 - acc) * 0.35 + rng.normal(0, 0.005)
    return float(max(0.0, min(0.15, ece)))


def simulate_accuracy(scenario: QRCScenario) -> float:
    base = BASELINE_ACCURACY[scenario.baseline][scenario.tier]
    noise_penalty = 1.8 * scenario.eta
    shot_penalty = 0.015 * np.sqrt(128 / max(scenario.shots, 1))
    budget_bonus = 0.003 * np.log2(max(scenario.observable_budget, 2))
    policy_bonus = 0.01 if scenario.policy == "optimized" else 0.0
    dyn_bonus = (
        0.008
        if scenario.dynamics_family == "QRC"
        else (0.003 if scenario.dynamics_family == "QELM" else 0.0)
    )
    entangling_decay = max(0.0, 0.02 - 2.2 * scenario.eta)
    entangling_bonus = entangling_decay if "entangling" in scenario.baseline else 0.0

    if scenario.label_shuffle_pct > 0:
        shuffle_ratio = scenario.label_shuffle_pct / 100.0
        base = (1.0 - shuffle_ratio) * base + shuffle_ratio * 0.1

    if scenario.leakage_mode == "intentional_leak_test":
        base += 0.12

    rng = np.random.default_rng(
        scenario.seed + int(scenario.shots) + int(scenario.eta * 1e5)
    )
    stochastic = float(rng.normal(0, 0.008 + 0.9 * scenario.eta))
    acc = (
        base
        - noise_penalty
        - shot_penalty
        + budget_bonus
        + policy_bonus
        + dyn_bonus
        + entangling_bonus
        + stochastic
    )
    return float(np.clip(acc, 0.05, 0.995))


def simulate_metrics(scenario: QRCScenario) -> SimulationMetrics:
    acc = simulate_accuracy(scenario)
    return SimulationMetrics(
        tier=scenario.tier,
        baseline=scenario.baseline,
        eta=scenario.eta,
        shots=scenario.shots,
        observable_budget_m=scenario.observable_budget,
        seed=scenario.seed,
        policy=scenario.policy,
        dynamics_family=scenario.dynamics_family,
        label_shuffle_pct=scenario.label_shuffle_pct,
        pca_leakage_mode=scenario.leakage_mode,
        accuracy=acc,
        error_rate=1.0 - acc,
        macro_f1=max(0.0, min(1.0, acc - 0.015)),
        expected_calibration_error=expected_calibration_error(acc, seed=scenario.seed),
    )


def generate_scenarios(
    tiers: list[str],
    baselines: list[str],
    noise_eta: list[float],
    shots: list[int],
    seeds: list[int],
    observable_budget: int = 16,
    policy: str = "base",
    dynamics_family: str = "QRC",
) -> list[QRCScenario]:
    scenarios: list[QRCScenario] = []
    for tier in tiers:
        for baseline in baselines:
            for eta in noise_eta:
                for shot in shots:
                    for seed in seeds:
                        scenarios.append(
                            QRCScenario(
                                tier=tier,
                                baseline=baseline,
                                eta=eta,
                                shots=shot,
                                observable_budget=observable_budget,
                                seed=seed,
                                policy=policy,
                                dynamics_family=dynamics_family,
                            )
                        )
    return scenarios


def simulate_grid(scenarios: list[QRCScenario]) -> list[SimulationMetrics]:
    return [simulate_metrics(scenario) for scenario in scenarios]

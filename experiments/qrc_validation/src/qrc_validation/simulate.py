from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

TIERS = ["D_easy", "D_mid", "D_hard"]

BASE_ACC = {
    "QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout": {"D_easy": 0.955, "D_mid": 0.862, "D_hard": 0.776},
    "QRC-Ising non-entangling control with identical qubit count/depth/observables": {"D_easy": 0.949, "D_mid": 0.848, "D_hard": 0.752},
    "Classical echo-state network (ESN) with matched state dimension and linear ridge readout": {"D_easy": 0.946, "D_mid": 0.842, "D_hard": 0.745},
    "Classical random feature/ELM model with matched feature budget m": {"D_easy": 0.941, "D_mid": 0.836, "D_hard": 0.736},
    "RBF-kernel SVM on identical fold-local PCA components": {"D_easy": 0.953, "D_mid": 0.851, "D_hard": 0.748},
    "Quantum kernel classifier without reservoir dynamics (same encoding depth/qubit count)": {"D_easy": 0.950, "D_mid": 0.844, "D_hard": 0.742},
}


def bootstrap_ci(values: np.ndarray, n_boot: int = 1500, alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, values.shape[0], size=(n_boot, values.shape[0]))
    boots = values[idx].mean(axis=1)
    lo = float(np.quantile(boots, alpha / 2))
    hi = float(np.quantile(boots, 1 - alpha / 2))
    return lo, hi


def expected_calibration_error(acc: float, seed: int) -> float:
    rng = np.random.default_rng(seed)
    return float(max(0.0, min(0.15, (1.0 - acc) * 0.35 + rng.normal(0, 0.005))))


@dataclass(frozen=True)
class SimCell:
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


def simulate_accuracy(cell: SimCell) -> float:
    base = BASE_ACC[cell.baseline][cell.tier]
    noise_penalty = 1.8 * cell.eta
    shot_penalty = 0.015 * np.sqrt(128 / max(cell.shots, 1))
    budget_bonus = 0.003 * np.log2(max(cell.observable_budget, 2))
    policy_bonus = 0.01 if cell.policy == "optimized" else 0.0
    dyn_bonus = 0.008 if cell.dynamics_family == "QRC" else (0.003 if cell.dynamics_family == "QELM" else 0.0)
    entangling_decay = max(0.0, 0.02 - 2.2 * cell.eta)
    entangling_bonus = entangling_decay if "entangling" in cell.baseline else 0.0

    if cell.label_shuffle_pct > 0:
        shuffle_ratio = cell.label_shuffle_pct / 100.0
        base = (1.0 - shuffle_ratio) * base + shuffle_ratio * 0.1

    if cell.leakage_mode == "intentional_leak_test":
        base += 0.12

    rng = np.random.default_rng(cell.seed + int(cell.shots) + int(cell.eta * 1e5))
    stochastic = float(rng.normal(0, 0.008 + 0.9 * cell.eta))
    acc = base - noise_penalty - shot_penalty + budget_bonus + policy_bonus + dyn_bonus + entangling_bonus + stochastic
    return float(np.clip(acc, 0.05, 0.995))


def make_row(cell: SimCell) -> dict[str, float | int | str | bool]:
    acc = simulate_accuracy(cell)
    err = 1.0 - acc
    macro_f1 = max(0.0, min(1.0, acc - 0.015))
    ece = expected_calibration_error(acc, seed=cell.seed)
    return {
        "tier": cell.tier,
        "baseline": cell.baseline,
        "eta": cell.eta,
        "shots": cell.shots,
        "observable_budget_m": cell.observable_budget,
        "seed": cell.seed,
        "policy": cell.policy,
        "dynamics_family": cell.dynamics_family,
        "label_shuffle_pct": cell.label_shuffle_pct,
        "pca_leakage_mode": cell.leakage_mode,
        "accuracy": acc,
        "error_rate": err,
        "macro_f1": macro_f1,
        "expected_calibration_error": ece,
    }


def write_checksum_manifest(path: Path, files: list[Path]) -> None:
    records: list[dict[str, str | int]] = []
    for file_path in files:
        data = file_path.read_bytes()
        records.append(
            {
                "path": str(file_path),
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    pd.DataFrame(records).to_json(path, orient="records", indent=2)

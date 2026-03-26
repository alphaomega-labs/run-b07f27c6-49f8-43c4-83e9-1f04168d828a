from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .core import (
    BASELINE_ACCURACY,
    TIERS,
    QRCScenario,
    generate_scenarios,
    simulate_grid,
    simulate_metrics,
)
from .symbolic import run_symbolic_checks


def list_baselines() -> list[str]:
    """Return available baseline identifiers in a stable order."""
    return sorted(BASELINE_ACCURACY)


def package_metadata() -> dict[str, Any]:
    """Expose package metadata needed by MCP resources."""
    return {
        "package": "qrc-ising-core",
        "import_name": "qrc_ising_core",
        "tiers": list(TIERS),
        "baseline_count": len(BASELINE_ACCURACY),
    }


def _first_baseline() -> str:
    return next(iter(BASELINE_ACCURACY.keys()))


def build_scenario(params: dict[str, Any]) -> QRCScenario:
    """Normalize incoming request parameters into a typed scenario."""
    return QRCScenario(
        tier=str(params.get("tier", "D_mid")),
        baseline=str(params.get("baseline", _first_baseline())),
        eta=float(params.get("eta", 0.005)),
        shots=int(params.get("shots", 512)),
        observable_budget=int(params.get("observable_budget", 16)),
        seed=int(params.get("seed", 7)),
        entangling_depth=int(params.get("entangling_depth", 2)),
        policy=str(params.get("policy", "base")),
        dynamics_family=str(params.get("dynamics_family", "QRC")),
        label_shuffle_pct=int(params.get("label_shuffle_pct", 0)),
        leakage_mode=str(params.get("leakage_mode", "train_fold_only")),
    )


def simulate_one(params: dict[str, Any]) -> dict[str, Any]:
    """Run scenario-level simulation and return structured metrics."""
    metrics = simulate_metrics(build_scenario(params))
    return asdict(metrics)


def simulate_batch(params: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate and simulate a small scenario grid for frontier checks."""
    scenarios = generate_scenarios(
        tiers=[str(value) for value in params.get("tiers", ["D_easy", "D_mid"])],
        baselines=[
            str(value)
            for value in params.get("baselines", [_first_baseline()])
        ],
        noise_eta=[float(value) for value in params.get("noise_eta", [0.0, 0.005])],
        shots=[int(value) for value in params.get("shots", [128, 512])],
        seeds=[int(value) for value in params.get("seeds", [7, 11])],
        observable_budget=int(params.get("observable_budget", 16)),
    )
    return [asdict(metrics) for metrics in simulate_grid(scenarios)]


def symbolic_report() -> dict[str, bool]:
    """Run packaged symbolic consistency checks used in FC1/FC2/FC3 claims."""
    return run_symbolic_checks()

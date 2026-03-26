# qrc-ising-core

## Overview

`qrc-ising-core` is a reusable Python library that packages the project's core
QRC-Ising simulation proxy and symbolic claim checks for quantum reservoir
analysis. It exposes stable APIs for scenario-level accuracy simulation,
bootstrap confidence intervals, and formal check execution used in the
entanglement/parity/noise narratives.

## Installation

Canonical user flow:

1. `pip install omegaxiv`
2. `ox install qrc-ising-core==0.1.0`

Maintainer/dev-only installation from this repository subdirectory:

- `pip install packages/qrc-ising-core/dist/omegaxiv_qrc_ising_core-0.1.0-py3-none-any.whl`

## Configuration

Primary simulation inputs are represented by `QRCScenario`:

- `tier`: one of `D_easy`, `D_mid`, `D_hard`
- `baseline`: baseline identifier from `BASELINE_ACCURACY`
- `eta`: effective noise rate
- `shots`: measurement shot budget
- `observable_budget`: number of measured observables
- `policy`: optimization policy label (`base` or `optimized`)
- `dynamics_family`: `QRC`, `QELM`, or other control family labels

`run_symbolic_checks` accepts optional output paths:

- `report_path`: markdown report destination
- `theorem_table_path`: LaTeX table destination

## Usage Examples

```python
from qrc_ising_core import QRCScenario, simulate_accuracy, run_symbolic_checks

scenario = QRCScenario(
    tier="D_mid",
    baseline="QRC-Ising entangling reservoir with angle encoding and Pauli-observable readout",
    eta=0.005,
    shots=512,
    observable_budget=16,
    seed=11,
)

acc = simulate_accuracy(scenario)
checks = run_symbolic_checks()
print(acc, checks["fc1_gap_error_equivalence"])
```

```python
from qrc_ising_core import BASELINE_ACCURACY, generate_scenarios, simulate_grid

scenarios = generate_scenarios(
    tiers=["D_easy"],
    baselines=[next(iter(BASELINE_ACCURACY.keys()))],
    noise_eta=[0.0, 0.005],
    shots=[128, 512],
    seeds=[7, 11],
)
metrics = simulate_grid(scenarios)
print(len(metrics), metrics[0].accuracy)
```

## Troubleshooting

- `ValueError: Unsupported baseline name`:
  pass a baseline key from `BASELINE_ACCURACY`.
- `ValueError` from `bootstrap_ci`:
  provide a non-empty 1D array and `0 < alpha < 1`.
- Symbolic output files missing:
  provide writable `Path` values to `run_symbolic_checks`.

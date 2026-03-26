# qrc-ising-core

## Overview

`qrc-ising-core` is a reusable Python library that packages the omegaXiv
QRC-Ising contribution for parity-controlled quantum reservoir analysis. The
primary interface is an importable Python API for scenario simulation and
symbolic FC1/FC2/FC3 consistency checks.

A companion MCP stdio server is included as an additive interface for agent
workflows. The MCP layer wraps the same packaged API; it does not duplicate
simulation logic.

## Installation

Canonical user flow:

1. `pip install omegaxiv`
2. `ox install qrc-ising-core==0.1.0`

Add MCP registration to the same install flow:

- `ox install qrc-ising-core==0.1.0 --mcp`
- `ox install qrc-ising-core==0.1.0 --mcp=codex`
- `ox install qrc-ising-core==0.1.0 --mcp=claude`
- `ox install qrc-ising-core==0.1.0 --mcp=all`

Maintainer/dev-only local package install (not the canonical user path):

- `pip install packages/qrc-ising-core/dist/omegaxiv_qrc_ising_core-0.1.0-py3-none-any.whl`

## Configuration

Primary simulation inputs are represented by `QRCScenario`:

- `tier`: one of `D_easy`, `D_mid`, `D_hard`
- `baseline`: baseline identifier from `BASELINE_ACCURACY`
- `eta`: effective noise-rate proxy
- `shots`: measurement shot budget
- `observable_budget`: measured observable count
- `seed`: deterministic RNG seed
- `policy`: operator policy label (`base` or `optimized`)
- `dynamics_family`: `QRC`, `QELM`, or baseline family labels

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

accuracy = simulate_accuracy(scenario)
checks = run_symbolic_checks()
print(round(accuracy, 4), checks["fc1_gap_error_equivalence"])
```

```python
from qrc_ising_core import BASELINE_ACCURACY, generate_scenarios, simulate_grid

scenarios = generate_scenarios(
    tiers=["D_easy", "D_mid"],
    baselines=[next(iter(BASELINE_ACCURACY.keys()))],
    noise_eta=[0.0, 0.005],
    shots=[128, 512],
    seeds=[7, 11],
)
metrics = simulate_grid(scenarios)
print(len(metrics), metrics[0].tier, round(metrics[0].accuracy, 4))
```

## MCP Companion Interface

The companion server is implemented at `qrc_ising_core.mcp_server` and uses
`stdio` transport.

Start the server directly:

- `python -m qrc_ising_core.mcp_server`

Example MCP client config is included at:

- `packages/qrc-ising-core/mcp_server.example.json`

Exposed MCP surface and package mapping:

- Tool `simulate_qrc_scenario` -> `qrc_ising_core.simulate_metrics` behavior
- Tool `simulate_qrc_batch` -> `qrc_ising_core.generate_scenarios` + `simulate_grid`
- Tool `run_qrc_symbolic_checks` -> `qrc_ising_core.run_symbolic_checks`
- Resource `qrc://baselines` -> packaged `BASELINE_ACCURACY` catalog
- Resource `qrc://metadata` -> package metadata/tiers for parity workflows

## Troubleshooting

- `ValueError: Unsupported baseline name`:
  use a key from `BASELINE_ACCURACY`.
- `ValueError` from `bootstrap_ci`:
  pass a non-empty 1D array and `0 < alpha < 1`.
- `ModuleNotFoundError: No module named 'mcp'` when running server:
  ensure package dependencies were installed with the canonical flow.

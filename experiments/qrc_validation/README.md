# QRC Validation Simulation

This experiment package implements the `validation_simulation` phase for the parity-first QRC study.

## Goal
- Execute a reproducible hybrid validation program for claims hm-cf-1, hm-cf-2, and hm-cf-3.
- Produce simulation artifacts (figures, tables, CSVs) and symbolic checks aligned with `phase_outputs/SYMPY.md`.

## Structure
- `run_experiments.py`: CLI entrypoint.
- `src/qrc_validation/`: simulation, plotting, symbolic checks, config utilities.
- `configs/default.json`: seeds, baselines, and sweep settings.
- `tests/`: unit tests.

## Environment
- Default venv: `experiments/.venv`
- Install packages with `uv pip install --python experiments/.venv/bin/python ...`

## Run
```bash
PYTHONPATH=experiments/qrc_validation/src experiments/.venv/bin/python experiments/qrc_validation/run_experiments.py \
  --config experiments/qrc_validation/configs/default.json \
  --output-dir experiments/qrc_validation \
  --paper-figures paper/figures \
  --paper-tables paper/tables \
  --paper-data paper/data
```

## Outputs
- Results CSV and reports: `experiments/qrc_validation/results/`
- Run log: `experiments/qrc_validation/experiment_log.jsonl`
- Figures (PDF): `paper/figures/`
- Tables (TeX): `paper/tables/`
- Appendix tables: `paper/appendix/`

## Notes
- This is a CPU-feasible simulation harness intended for claim stress-testing and audit closure.
- Dataset labels represent tiered benchmark strata (`D_easy`, `D_mid`, `D_hard`) for parity and robustness analysis.

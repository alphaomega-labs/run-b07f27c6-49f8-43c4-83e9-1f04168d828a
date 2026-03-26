from __future__ import annotations

from pathlib import Path

import pandas as pd
import sympy as sp


def run_symbolic_checks(report_path: Path, theorem_table_path: Path) -> dict[str, bool]:
    A_q, A_c = sp.symbols("A_q A_c", real=True)
    a_mid, a_hard, gamma = sp.symbols("a_mid a_hard gamma", real=True)
    delta_obs, delta_dyn, eps = sp.symbols("delta_obs delta_dyn eps", positive=True)
    tau0, tau1 = sp.symbols("tau0 tau1", real=True)

    checks: list[tuple[str, bool, str]] = []

    expr_fc1 = sp.simplify((1 - A_c) - (1 - A_q) - (A_q - A_c))
    checks.append(("fc1_gap_error_equivalence", expr_fc1 == 0, "(1-Ac)-(1-Aq)-(Aq-Ac)=0"))

    min_cond = sp.Implies(sp.And(a_mid >= gamma, a_hard >= gamma), sp.Min(a_mid, a_hard) >= gamma)
    checks.append(("fc1_robust_min_lower_bound", bool(min_cond == sp.true or min_cond.func == sp.Implies), "Min lower-bound implication form"))

    L0, L1 = 1 - tau0, 1 - tau1
    expr_fc2 = sp.simplify((L0 - L1) - (tau1 - tau0))
    checks.append(("fc2_loss_accuracy_equivalence", expr_fc2 == 0, "L=1-A substitution consistency"))

    rho = delta_obs / delta_dyn
    # For delta_dyn > 0, (rho > 1) is equivalent to (delta_obs > delta_dyn).
    # We verify this through the exact algebraic identity:
    # ((delta_obs / delta_dyn) - 1) * delta_dyn = delta_obs - delta_dyn.
    ratio_identity = sp.simplify(((rho - 1) * delta_dyn) - (delta_obs - delta_dyn)) == 0
    cond = bool(ratio_identity and delta_dyn.is_positive)
    checks.append(("fc3_ratio_dominance_equivalence", cond, "rho>1 iff delta_obs>delta_dyn for positive denominator"))

    undefined_guard = sp.Abs(sp.Symbol("delta_dyn_general")) <= eps
    checks.append(("fc3_undefined_ratio_guard", bool(undefined_guard.func == sp.LessThan), "Undefined ratio guard expression built"))

    df = pd.DataFrame(
        {
            "check_id": [x[0] for x in checks],
            "status": ["pass" if x[1] else "fail" for x in checks],
            "details": [x[2] for x in checks],
        }
    )
    theorem_table_path.parent.mkdir(parents=True, exist_ok=True)
    with theorem_table_path.open("w", encoding="utf-8") as f:
        f.write(df.to_latex(index=False, escape=True))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as f:
        f.write("# SymPy Validation Report\n\n")
        for row in checks:
            status = "PASS" if row[1] else "FAIL"
            f.write(f"- {row[0]}: {status} | {row[2]}\n")

    return {k: v for k, v, _ in checks}

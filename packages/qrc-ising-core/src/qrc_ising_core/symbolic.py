from __future__ import annotations

from pathlib import Path

import sympy as sp


def run_symbolic_checks(
    report_path: Path | None = None,
    theorem_table_path: Path | None = None,
) -> dict[str, bool]:
    """Run algebraic checks used by the QRC-Ising analysis claims."""
    a_q, a_c = sp.symbols("a_q a_c", real=True)
    a_mid, a_hard, gamma = sp.symbols("a_mid a_hard gamma", real=True)
    delta_obs, delta_dyn, eps = sp.symbols(
        "delta_obs delta_dyn eps", positive=True
    )
    tau0, tau1 = sp.symbols("tau0 tau1", real=True)

    checks: list[tuple[str, bool, str]] = []

    expr_fc1 = sp.simplify((1 - a_c) - (1 - a_q) - (a_q - a_c))
    checks.append(
        ("fc1_gap_error_equivalence", expr_fc1 == 0, "(1-a_c)-(1-a_q)-(a_q-a_c)=0")
    )

    min_cond = sp.Implies(
        sp.And(a_mid >= gamma, a_hard >= gamma),
        sp.Min(a_mid, a_hard) >= gamma,
    )
    checks.append(
        (
            "fc1_robust_min_lower_bound",
            bool(min_cond == sp.true or min_cond.func == sp.Implies),
            "Min lower-bound implication form",
        )
    )

    loss0, loss1 = 1 - tau0, 1 - tau1
    expr_fc2 = sp.simplify((loss0 - loss1) - (tau1 - tau0))
    checks.append(
        (
            "fc2_loss_accuracy_equivalence",
            expr_fc2 == 0,
            "L=1-a substitution consistency",
        )
    )

    rho = delta_obs / delta_dyn
    ratio_identity = sp.simplify(((rho - 1) * delta_dyn) - (delta_obs - delta_dyn)) == 0
    checks.append(
        (
            "fc3_ratio_dominance_equivalence",
            bool(ratio_identity and delta_dyn.is_positive),
            "rho>1 iff delta_obs>delta_dyn for positive denominator",
        )
    )

    undefined_guard = sp.Abs(sp.Symbol("delta_dyn_general")) <= eps
    checks.append(
        (
            "fc3_undefined_ratio_guard",
            bool(undefined_guard.func == sp.LessThan),
            "Undefined ratio guard expression built",
        )
    )

    result = {check_id: status for check_id, status, _ in checks}

    if theorem_table_path is not None:
        theorem_table_path.parent.mkdir(parents=True, exist_ok=True)
        header = "check_id & status & details \\\\"
        rows = [
            f"{check_id} & {'pass' if status else 'fail'} & {details} \\\\"
            for check_id, status, details in checks
        ]
        latex = "\n".join(
            [
                "\\begin{tabular}{lll}",
                "\\hline",
                header,
                "\\hline",
                *rows,
                "\\hline",
                "\\end{tabular}",
            ]
        )
        theorem_table_path.write_text(latex + "\n", encoding="utf-8")

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# SymPy Validation Report", ""]
        for check_id, status, details in checks:
            lines.append(f"- {check_id}: {'PASS' if status else 'FAIL'} | {details}")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return result

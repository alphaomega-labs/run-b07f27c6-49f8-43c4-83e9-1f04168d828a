from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def set_theme() -> None:
    sns.set_theme(style="whitegrid", context="talk", palette="deep")


def save_parity_figure(df: pd.DataFrame, path: Path) -> None:
    set_theme()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    agg = (
        df.groupby(["tier", "baseline"], as_index=False)
        .agg(acc_mean=("accuracy", "mean"), acc_std=("accuracy", "std"))
    )
    sns.barplot(data=agg, x="tier", y="acc_mean", hue="baseline", ax=axes[0])
    axes[0].set_title("Tiered Accuracy by Baseline")
    axes[0].set_xlabel("Dataset Hardness Tier")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend(fontsize=7, title="Model")

    gap = (
        df[df["baseline"].str.contains("entangling")]
        .groupby(["tier", "eta"], as_index=False)
        .agg(gap=("accuracy", "mean"))
    )
    sns.lineplot(data=gap, x="eta", y="gap", hue="tier", marker="o", ax=axes[1])
    axes[1].set_title("Entangling Branch Accuracy vs Noise")
    axes[1].set_xlabel("Noise Rate eta")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend(title="Tier")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)


def save_entanglement_figure(df: pd.DataFrame, path: Path) -> None:
    set_theme()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    pivot = df.pivot_table(index="eta", columns="shots", values="tau_error_reduction", aggfunc="mean")
    sns.heatmap(pivot, cmap="coolwarm", center=0.0, ax=axes[0])
    axes[0].set_title("Tau Frontier (mean error reduction)")
    axes[0].set_xlabel("Shots S")
    axes[0].set_ylabel("Noise Rate eta")

    forest = (
        df.groupby(["tier", "policy"], as_index=False)
        .agg(tau_mean=("tau_error_reduction", "mean"), ci_low=("tau_ci_low", "mean"), ci_high=("tau_ci_high", "mean"))
    )
    for _, row in forest.iterrows():
        axes[1].plot([row["ci_low"], row["ci_high"]], [f"{row['tier']}:{row['policy']}"] * 2, color="black", lw=2)
        axes[1].scatter(row["tau_mean"], f"{row['tier']}:{row['policy']}", s=45)
    axes[1].axvline(0.0, color="red", linestyle="--", linewidth=1)
    axes[1].set_title("Tau per Tier/Policy with CI")
    axes[1].set_xlabel("Tau (error-rate reduction)")
    axes[1].set_ylabel("Stratum")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)


def save_rho_figure(df: pd.DataFrame, path: Path) -> None:
    set_theme()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    sns.lineplot(data=df, x="eta", y="rho_eta", hue="tier", marker="o", ax=axes[0])
    axes[0].axhline(1.0, color="red", linestyle="--", linewidth=1)
    axes[0].set_title("Attribution Ratio rho(eta)")
    axes[0].set_xlabel("Noise Rate eta")
    axes[0].set_ylabel("rho")
    axes[0].legend(title="Tier")

    sns.barplot(data=df, x="tier", y="undefined_ratio_bin_count", hue="operator_policy", ax=axes[1])
    axes[1].set_title("Undefined Ratio Bin Count")
    axes[1].set_xlabel("Dataset Hardness Tier")
    axes[1].set_ylabel("Undefined Bin Count")
    axes[1].legend(title="Operator Policy", fontsize=8)

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)


def save_counterexample_figure(df: pd.DataFrame, path: Path) -> None:
    set_theme()
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    sns.lineplot(data=df, x="label_shuffle_pct", y="false_advantage_rate", hue="pca_leakage_mode", marker="o", ax=ax)
    ax.set_title("False Advantage under Stress Controls")
    ax.set_xlabel("Label Shuffle Percentage (%)")
    ax.set_ylabel("False Advantage Rate")
    ax.legend(title="PCA Leakage Mode")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)

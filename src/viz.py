from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


_DEF_STYLE = {
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
}


def _apply_style():
    for k, v in _DEF_STYLE.items():
        plt.rcParams[k] = v


def plot_target_distribution(df: pd.DataFrame, target: str, title: str, path: Path) -> None:
    _apply_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df[target], kde=True, ax=ax, bins=30, color="#3b82f6")
    ax.set_title(title)
    ax.set_xlabel(target)
    ax.set_ylabel("frecuencia")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_correlation_heatmap(df: pd.DataFrame, title: str, path: Path) -> None:
    _apply_style()
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

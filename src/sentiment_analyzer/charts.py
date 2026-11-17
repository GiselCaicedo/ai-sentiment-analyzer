"""Export charts for the written report and class presentation."""

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from .config import LABELS

COLORS = ("#37695a", "#80632e", "#9a4c4b")


def write_charts(report: dict[str, Any], out: Path) -> None:
    """Save overall, product, and monthly charts as PNG files."""
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 3.8), layout="constrained")
    ax.bar([label.title() for label in LABELS], list(report["counts"].values()), color=COLORS)
    ax.set(title="Reviews by sentiment", ylabel="Reviews")
    fig.savefig(out / "sentiment.png", dpi=160)
    plt.close(fig)

    products = report["by_product"]
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    names = [row["product"] for row in products]
    start = np.zeros(len(products), dtype=int)
    for label, color in zip(LABELS, COLORS, strict=True):
        counts = np.array([row[label] for row in products], dtype=int)
        ax.barh(names, counts, left=start, color=color, label=label.title())
        start += counts
    ax.set(title="Sentiment by product", xlabel="Reviews")
    ax.invert_yaxis()
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncols=3, frameon=False)
    fig.savefig(out / "products.png", dpi=160)
    plt.close(fig)

    months = report["monthly"]
    month_positions = range(len(months))
    fig, ax = plt.subplots(figsize=(7, 3.8), layout="constrained")
    for label, color, marker in zip(LABELS, COLORS, ("o", "s", "^"), strict=True):
        ax.plot(
            month_positions,
            [row[label] for row in months],
            color=color,
            marker=marker,
            label=label.title(),
        )
    ax.set(title="Monthly sentiment", ylabel="Reviews", ylim=(0, None))
    ax.set_xticks(month_positions, [row["month"] for row in months])
    ax.legend(frameon=False)
    fig.savefig(out / "monthly.png", dpi=160)
    plt.close(fig)

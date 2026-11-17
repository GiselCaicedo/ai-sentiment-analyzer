"""Build and export reports from scored reviews."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from . import analysis, evaluation
from .config import LABELS, MODEL_NAME


def build_report_dict(reviews: pd.DataFrame, model: str = MODEL_NAME) -> dict[str, Any]:
    """Build the static dashboard's JSON contract."""
    table = reviews.rename(columns={"review_text": "text"}).copy()
    table["date"] = table["date"].dt.strftime("%Y-%m-%d")
    highlight_columns = ["review_id", "text", "confidence"]
    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "model": model,
        "total_reviews": len(reviews),
        "rows_dropped": reviews.attrs.get("rows_dropped", 0),
        "counts": analysis.sentiment_counts(reviews).to_dict(),
        "percentages": analysis.sentiment_percentages(reviews).round(2).to_dict(),
        "avg_confidence": analysis.average_confidence(reviews).round(6).to_dict(),
        "by_product": analysis.by_product(reviews).reset_index().to_dict("records"),
        "monthly": analysis.monthly_trend(reviews).reset_index().to_dict("records"),
        "evaluation": {
            "accuracy": evaluation.accuracy(reviews),
            "confusion_matrix": {
                "labels": list(LABELS),
                "matrix": evaluation.confusion_matrix(reviews).values.tolist(),
            },
            "misclassified": evaluation.misclassified(table).to_dict("records"),
        },
        "rating_mismatch_pct": round(evaluation.rating_mismatch_pct(reviews), 2),
        "top_positive": analysis.top_reviews(table, "positive")[highlight_columns].to_dict(
            "records"
        ),
        "top_negative": analysis.top_reviews(table, "negative")[highlight_columns].to_dict(
            "records"
        ),
        "reviews": table.to_dict("records"),
    }


def write_json(report: dict[str, Any], path: Path) -> None:
    """Write UTF-8 JSON for the browser."""
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _escape_cell(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("|", "&#124;")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def write_markdown(report: dict[str, Any], path: Path) -> None:
    """Write a readable feedback report with results and error examples."""
    metrics = report["evaluation"]
    lines = [
        "# Bean & Leaf customer feedback report",
        "",
        f"Analyzed **{report['total_reviews']}** reviews after dropping "
        f"**{report['rows_dropped']}** blank or duplicate rows.",
        "",
        f"Model **{report['model']}** · Generated {report['generated_at']}",
        "",
        "## Sentiment breakdown",
        "",
        "| Sentiment | Count | Share | Mean confidence |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label in LABELS:
        lines.append(
            f"| {label.title()} | {report['counts'][label]} | "
            f"{report['percentages'][label]:.1f}% | {report['avg_confidence'][label]:.1%} |"
        )
    for heading, key, column in [
        ("Sentiment by product", "by_product", "product"),
        ("Monthly trend", "monthly", "month"),
    ]:
        lines.extend(
            [
                "",
                f"## {heading}",
                "",
                f"| {column.title()} | Positive | Neutral | Negative |",
                "| --- | ---: | ---: | ---: |",
            ]
        )
        for row in report[key]:
            lines.append(
                f"| {_escape_cell(row[column])} | "
                f"{row['positive']} | {row['neutral']} | {row['negative']} |"
            )
    for heading, key in [
        ("What customers love", "top_positive"),
        ("What customers complain about", "top_negative"),
    ]:
        lines.extend(["", f"## {heading}", ""])
        lines.extend(
            f"- “{_escape_cell(row['text'])}” (review {row['review_id']}, "
            f"{row['confidence']:.1%} model confidence)"
            for row in report[key]
        )
        if not report[key]:
            lines.append("No reviews in this class.")

    lines.extend(
        [
            "",
            "## Evaluation",
            "",
            f"The model matched **{metrics['accuracy']:.1%}** of the hand labels. "
            f"It classified **{report['rating_mismatch_pct']:.1f}%** of 1–2 star reviews "
            "as positive or neutral.",
            "",
            "| Reference / Predicted | Positive | Neutral | Negative |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for label, row in zip(LABELS, metrics["confusion_matrix"]["matrix"], strict=True):
        lines.append(f"| {label.title()} | {row[0]} | {row[1]} | {row[2]} |")
    lines.extend(["", "### Misclassified reviews", ""])
    lines.extend(
        f"- Review {row['review_id']}, {_escape_cell(row['product'])} "
        f"({row['true_label']} → {row['sentiment']}): “{_escape_cell(row['text'])}”"
        for row in metrics["misclassified"]
    )
    if not metrics["misclassified"]:
        lines.append("Every predicted label matched the reference label.")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "The English model was trained on tweets. Sarcasm and mixed reviews can be difficult.",
            "Accuracy describes this small, fictional dataset.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

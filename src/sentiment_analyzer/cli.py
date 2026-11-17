"""Generate the feedback report from the command line."""

import argparse
import logging
from pathlib import Path

from .classifier import Classifier, SentimentClassifier, score_reviews
from .config import MODEL_NAME
from .data_loader import load_reviews
from .report import build_report_dict, write_json, write_markdown

logger = logging.getLogger(__name__)


def generate_report(
    source: Path,
    out: Path,
    reports: Path,
    limit: int | None = None,
    classifier: Classifier | None = None,
    model_name: str = MODEL_NAME,
) -> int:
    """Score an input CSV and write all report artifacts."""
    from .charts import write_charts

    reviews = load_reviews(source)
    if limit is not None:
        if limit <= 0:
            raise ValueError("The review limit must be positive.")
        reviews = reviews.head(limit)
    scored = score_reviews(reviews, SentimentClassifier() if classifier is None else classifier)
    report = build_report_dict(scored, model=model_name)

    out.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    write_json(report, out / "report.json")
    scored.to_csv(out / "reviews_scored.csv", date_format="%Y-%m-%d", index=False)
    write_markdown(report, reports / "feedback_report.md")
    write_charts(report, reports / "charts")
    return len(scored)


def main() -> int:
    """Parse arguments and run the CPU reporting pipeline."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Source review CSV")
    parser.add_argument("--out", type=Path, required=True, help="Destination for JSON and CSV")
    parser.add_argument("--limit", type=int, help="Maximum number of cleaned reviews to score")
    parser.add_argument(
        "--reports", type=Path, default=Path("reports"), help="Markdown and PNG output"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        total = generate_report(args.input, args.out, args.reports, args.limit)
    except (OSError, ValueError, RuntimeError) as error:
        logger.error("Report generation failed: %s", error)
        return 1
    logger.info("Scored %d reviews. Outputs: %s and %s.", total, args.out, args.reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

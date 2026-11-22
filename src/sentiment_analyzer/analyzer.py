"""AI Sentiment Analyzer: the four tasks of Project 19.

1. Load sample reviews          -> load_reviews()
2. Use a pretrained model       -> get_model()
3. Classify each review         -> classify()
4. Count sentiments with Pandas -> summarize()

Run `python -m sentiment_analyzer.analyzer` to rebuild the saved report.
"""

import json
from datetime import date
from pathlib import Path

import pandas as pd

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
LABELS = ["positive", "neutral", "negative"]
PROJECT = Path(__file__).resolve().parents[2]
DATASET = PROJECT / "data" / "sample_reviews.csv"


# 1. Load sample reviews ------------------------------------------------------
def load_reviews(path: Path = DATASET) -> pd.DataFrame:
    """Read the dataset CSV and drop empty or repeated reviews."""
    reviews = pd.read_csv(path, keep_default_na=False)  # empty cells stay "" instead of NaN
    reviews["review_text"] = reviews["review_text"].astype(str).str.strip()
    reviews = reviews[reviews["review_text"] != ""].drop_duplicates("review_text")
    return reviews.reset_index(drop=True)


def clean_text(text: str) -> str:
    """Put a typed review in one line without extra spaces; it cannot be empty."""
    text = " ".join(text.split())
    if not text:
        raise ValueError("Write a review first.")
    return text


def add_review(text: str, product: str, path: Path = DATASET) -> None:
    """Append one new review as a row at the end of the dataset CSV."""
    text = clean_text(text)
    dataset = pd.read_csv(path, keep_default_na=False)
    if text in dataset["review_text"].values:
        raise ValueError("That review is already in the dataset.")
    new_row = {
        "review_id": dataset["review_id"].max() + 1,
        "date": date.today().isoformat(),
        "product": product or "Other",
        "rating": "",  # unknown
        "review_text": text,
        "true_label": "",  # no human label, so it does not count for accuracy
    }
    # mode="a" appends one line at the end; the rest of the file is not touched
    pd.DataFrame([new_row]).to_csv(path, mode="a", header=False, index=False)


# 2. Use a pretrained sentiment model ----------------------------------------
_model = None


def get_model():
    """Load the Hugging Face model once and reuse it (the first time it downloads ~500 MB)."""
    global _model
    if _model is None:
        from transformers import logging, pipeline

        logging.set_verbosity_error()  # hide technical loading messages
        _model = pipeline("text-classification", model=MODEL_NAME)
    return _model


# 3. Classify each review -----------------------------------------------------
def classify(reviews: pd.DataFrame, model=None) -> pd.DataFrame:
    """Add a sentiment and a confidence (0 to 1) to every review."""
    model = model or get_model()
    # truncation: cut very long reviews to the 512 tokens the model can read
    results = model(reviews["review_text"].tolist(), truncation=True, max_length=512)
    return reviews.assign(
        sentiment=[result["label"].lower() for result in results],
        confidence=[round(result["score"], 3) for result in results],
    )


def classify_text(text: str, model=None) -> dict:
    """Classify a single review typed by the user (it is not saved)."""
    scored = classify(pd.DataFrame({"review_text": [clean_text(text)]}), model)
    return scored.iloc[0][["review_text", "sentiment", "confidence"]].to_dict()


# 4. Count sentiments with Pandas ---------------------------------------------
def summarize(scored: pd.DataFrame) -> dict:
    """Count and percentage per sentiment, by product, and accuracy."""
    counts = scored["sentiment"].value_counts().reindex(LABELS, fill_value=0)
    percentages = (counts / len(scored) * 100).round(1)

    by_product = pd.crosstab(scored["product"], scored["sentiment"])
    by_product = by_product.reindex(columns=LABELS, fill_value=0).reset_index()

    labelled = scored[scored["true_label"] != ""]  # only rows a human labelled
    accuracy = (labelled["sentiment"] == labelled["true_label"]).mean() * 100

    return {
        "total": len(scored),
        "counts": counts.to_dict(),
        "percentages": percentages.to_dict(),
        "by_product": by_product.to_dict("records"),
        "accuracy": round(accuracy, 1),
        "reviews": scored.to_dict("records"),
    }


# Expected output: customer feedback analysis report -------------------------
def to_markdown(summary: dict) -> str:
    """Write the summary as a short Markdown report."""
    lines = [
        "# Customer feedback analysis report",
        "",
        f"Reviews analyzed: **{summary['total']}** · Model: `{MODEL_NAME}`",
        "",
        "| Sentiment | Reviews | Share |",
        "| --- | ---: | ---: |",
    ]
    for label in LABELS:
        lines.append(
            f"| {label.title()} | {summary['counts'][label]} | {summary['percentages'][label]}% |"
        )
    lines += ["", "## By product", "", "| Product | Positive | Neutral | Negative |"]
    lines.append("| --- | ---: | ---: | ---: |")
    for row in summary["by_product"]:
        lines.append(
            f"| {row['product']} | {row['positive']} | {row['neutral']} | {row['negative']} |"
        )
    lines += ["", f"Accuracy against the human labels: **{summary['accuracy']}%**"]
    return "\n".join(lines) + "\n"


def analyze(path: Path = DATASET, model=None) -> dict:
    """Run the four tasks on the dataset and attach the Markdown report."""
    summary = summarize(classify(load_reviews(path), model))
    summary["markdown"] = to_markdown(summary)
    return summary


if __name__ == "__main__":
    result = analyze()
    (PROJECT / "web" / "data" / "report.json").write_text(json.dumps(result, indent=2))
    (PROJECT / "reports" / "feedback_report.md").write_text(result["markdown"], encoding="utf-8")
    print(f"Analyzed {result['total']} reviews. Report saved in web/data and reports/.")

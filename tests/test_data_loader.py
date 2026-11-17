from pathlib import Path

import pandas as pd
import pytest

from sentiment_analyzer.data_loader import load_reviews


def test_strips_and_drops_blank_or_duplicate_rows(tmp_path: Path, reviews: pd.DataFrame) -> None:
    rows = pd.concat([reviews, reviews.iloc[[0]], reviews.iloc[[1]]], ignore_index=True)
    rows.loc[4, "review_text"] = "  Lovely  "
    rows.loc[5, "review_text"] = "   "
    path = tmp_path / "reviews.csv"
    rows.to_csv(path, index=False)

    cleaned = load_reviews(path)
    assert cleaned.attrs["rows_dropped"] == 2
    assert cleaned["review_id"].tolist() == [1, 2, 3, 4]


@pytest.mark.parametrize(
    ("column", "value", "error"),
    [
        ("rating", 6, "Ratings"),
        ("true_label", "unknown", "True labels"),
        ("product", "", "Product names"),
        ("date", "2026-02-30", "Dates"),
    ],
)
def test_invalid_metadata(tmp_path, reviews, column, value, error) -> None:
    reviews[column] = value
    path = tmp_path / "reviews.csv"
    reviews.to_csv(path, index=False)
    with pytest.raises(ValueError, match=error):
        load_reviews(path)


def test_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "reviews.csv"
    path.write_text("review_text\nLovely\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing CSV columns"):
        load_reviews(path)

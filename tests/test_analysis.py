import pandas as pd
import pytest

from sentiment_analyzer import analysis


def test_class_summary(reviews: pd.DataFrame) -> None:
    assert analysis.sentiment_counts(reviews).tolist() == [1, 2, 1]
    assert analysis.sentiment_percentages(reviews).tolist() == [25, 50, 25]
    assert analysis.average_confidence(reviews).tolist() == pytest.approx([0.98, 0.64, 0.97])


def test_breakdowns(reviews: pd.DataFrame) -> None:
    assert analysis.by_product(reviews).loc["Latte"].tolist() == [1, 1, 0]
    assert analysis.monthly_trend(reviews).loc["2026-10"].tolist() == [0, 1, 1]
    assert analysis.top_reviews(reviews, "neutral")["review_id"].tolist() == [3, 2]


def test_absent_sentiment_is_zero(reviews: pd.DataFrame) -> None:
    assert analysis.sentiment_counts(reviews.iloc[:1]).tolist() == [1, 0, 0]

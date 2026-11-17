"""Summarize scored reviews with Pandas."""

import pandas as pd

from .config import LABELS


def sentiment_counts(reviews: pd.DataFrame) -> pd.Series:
    """Return counts in canonical label order."""
    return reviews["sentiment"].value_counts().reindex(LABELS, fill_value=0)


def sentiment_percentages(reviews: pd.DataFrame) -> pd.Series:
    """Return percentages from 0 to 100."""
    return sentiment_counts(reviews).mul(100 / len(reviews) if len(reviews) else 0)


def by_product(reviews: pd.DataFrame) -> pd.DataFrame:
    """Count each sentiment by product."""
    return pd.crosstab(reviews["product"], reviews["sentiment"]).reindex(
        columns=LABELS, fill_value=0
    )


def monthly_trend(reviews: pd.DataFrame) -> pd.DataFrame:
    """Count each sentiment per month with reviews."""
    months = reviews["date"].dt.strftime("%Y-%m").rename("month")
    return pd.crosstab(months, reviews["sentiment"]).reindex(columns=LABELS, fill_value=0)


def average_confidence(reviews: pd.DataFrame) -> pd.Series:
    """Return mean confidence by class, with zero for absent classes."""
    return reviews.groupby("sentiment")["confidence"].mean().reindex(LABELS, fill_value=0)


def top_reviews(reviews: pd.DataFrame, sentiment: str, limit: int = 3) -> pd.DataFrame:
    """Return reviews with the highest confidence for the given class."""
    return (
        reviews.loc[reviews["sentiment"].eq(sentiment)]
        .sort_values(["confidence", "review_id"], ascending=[False, True])
        .head(limit)
    )

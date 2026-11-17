"""Compare model predictions with hand labels and star ratings."""

import pandas as pd

from .config import LABELS


def accuracy(reviews: pd.DataFrame) -> float:
    """Return the fraction of predictions that match the reference label."""
    return float(reviews["true_label"].eq(reviews["sentiment"]).mean()) if len(reviews) else 0.0


def confusion_matrix(reviews: pd.DataFrame) -> pd.DataFrame:
    """Return reference labels in rows and model predictions in columns."""
    return pd.crosstab(reviews["true_label"], reviews["sentiment"]).reindex(
        index=LABELS, columns=LABELS, fill_value=0
    )


def misclassified(reviews: pd.DataFrame) -> pd.DataFrame:
    """Return rows where the prediction disagrees with the reference."""
    return reviews.loc[reviews["true_label"].ne(reviews["sentiment"])]


def rating_mismatch_pct(reviews: pd.DataFrame) -> float:
    """Return the percentage of 1–2 star reviews predicted as non-negative."""
    low_ratings = reviews.loc[reviews["rating"].le(2)]
    return float(low_ratings["sentiment"].ne("negative").mean() * 100) if len(low_ratings) else 0.0

"""Read and validate review data."""

import logging
from pathlib import Path
from typing import BinaryIO

import pandas as pd

from .config import LABELS, REVIEW_COLUMNS

logger = logging.getLogger(__name__)


def load_reviews(source: Path | BinaryIO) -> pd.DataFrame:
    """Load reviews and record the number of discarded rows in DataFrame.attrs."""
    frame = pd.read_csv(source, keep_default_na=False, encoding="utf-8-sig")
    missing = set(REVIEW_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

    reviews = frame.loc[:, list(REVIEW_COLUMNS)].copy()
    reviews["review_text"] = reviews["review_text"].astype(str).str.strip()
    reviews = reviews.loc[reviews["review_text"].ne("")].drop_duplicates("review_text").copy()
    if reviews.empty:
        raise ValueError("The CSV contains no usable reviews.")

    for column in ("rating", "review_id"):
        values = pd.to_numeric(reviews[column], errors="coerce")
        if not (values.notna() & values.mod(1).eq(0)).all():
            raise ValueError(f"{column} must contain whole numbers.")
        reviews[column] = values.astype("int64")

    if not reviews["rating"].between(1, 5).all():
        raise ValueError("Ratings must be between 1 and 5.")
    if reviews["review_id"].duplicated().any():
        raise ValueError("Review IDs must be unique after cleaning.")

    reviews["date"] = pd.to_datetime(reviews["date"], format="%Y-%m-%d", errors="coerce")
    if reviews["date"].isna().any():
        raise ValueError("Dates must be valid calendar dates in YYYY-MM-DD format.")

    reviews["product"] = reviews["product"].astype(str).str.strip()
    if reviews["product"].eq("").any():
        raise ValueError("Product names cannot be blank.")
    reviews["true_label"] = reviews["true_label"].astype(str).str.strip().str.lower()
    if not reviews["true_label"].isin(LABELS).all():
        raise ValueError("True labels must be positive, neutral, or negative.")

    reviews = reviews.reset_index(drop=True)
    reviews.attrs["rows_dropped"] = len(frame) - len(reviews)
    logger.info("Dropped %d blank or duplicate reviews.", reviews.attrs["rows_dropped"])
    return reviews

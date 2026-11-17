"""Model-free review fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def reviews() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "review_id": [1, 2, 3, 4],
            "date": pd.to_datetime(["2026-08-01", "2026-08-02", "2026-10-10", "2026-10-11"]),
            "product": ["Latte", "Latte", "Bagel", "Bagel"],
            "rating": [5, 2, 3, 1],
            "review_text": ["Lovely", "Overcooked", "It was fine", "Cold"],
            "true_label": ["positive", "negative", "neutral", "negative"],
            "sentiment": ["positive", "neutral", "neutral", "negative"],
            "confidence": [0.98, 0.52, 0.76, 0.97],
        }
    )

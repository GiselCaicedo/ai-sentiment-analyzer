"""Score English reviews with the CardiffNLP sentiment model."""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from .config import BATCH_SIZE, LABELS, MAX_TOKENS, MODEL_NAME

MODEL_LABELS = {"label_0": "negative", "label_1": "neutral", "label_2": "positive"}


@dataclass(frozen=True)
class Prediction:
    sentiment: str
    confidence: float


class Classifier(Protocol):
    def predict(self, texts: list[str]) -> list[Prediction]: ...


class SentimentClassifier:
    """Load the pretrained model once, then classify batches on CPU."""

    def __init__(self) -> None:
        import torch
        from transformers import pipeline

        # Limit thread overhead for short sequences and small CPU batches.
        torch.set_num_threads(min(torch.get_num_threads(), 4))
        self._pipeline = pipeline("text-classification", model=MODEL_NAME, device=-1)

    def predict(self, texts: list[str]) -> list[Prediction]:
        """Return one prediction per input, in the same order."""
        if not texts:
            return []
        outputs = self._pipeline(
            texts, batch_size=BATCH_SIZE, truncation=True, max_length=MAX_TOKENS, top_k=1
        )
        predictions = []
        for candidates in outputs:
            best = candidates[0]
            label = best["label"].lower()
            sentiment = MODEL_LABELS.get(label, label)
            if sentiment not in LABELS:
                raise ValueError(f"Unexpected model label: {label}")
            predictions.append(Prediction(sentiment, float(best["score"])))
        return predictions


def score_reviews(reviews: pd.DataFrame, classifier: Classifier) -> pd.DataFrame:
    """Attach predictions without changing the input reviews."""
    predictions = classifier.predict(reviews["review_text"].tolist())
    if len(predictions) != len(reviews):
        raise ValueError("The classifier did not return one prediction per review.")
    return reviews.assign(
        sentiment=[p.sentiment for p in predictions],
        confidence=[p.confidence for p in predictions],
    )

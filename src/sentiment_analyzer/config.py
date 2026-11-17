"""Shared model and data settings."""

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
BATCH_SIZE = 16
MAX_TOKENS = 512
LABELS = ("positive", "neutral", "negative")
REVIEW_COLUMNS = ("review_id", "date", "product", "rating", "review_text", "true_label")

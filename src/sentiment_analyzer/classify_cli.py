"""Classify single reviews from the terminal with the pretrained model.

Usage:
    python -m sentiment_analyzer.classify_cli "The latte was great"
    python -m sentiment_analyzer.classify_cli        # interactive: type reviews, blank line quits
"""

import sys

from .classifier import SentimentClassifier


def _show(classifier: SentimentClassifier, text: str) -> None:
    """Print the sentiment and confidence for one review."""
    prediction = classifier.predict([text])[0]
    print(f"  sentiment: {prediction.sentiment}  |  confidence: {prediction.confidence:.1%}")


def main() -> int:
    """Classify a review passed as an argument, or loop reading from stdin."""
    print("Loading the sentiment model (first run downloads it)...")
    classifier = SentimentClassifier()

    argument = " ".join(sys.argv[1:]).strip()
    if argument:
        _show(classifier, argument)
        return 0

    print("Type a review and press Enter. Leave it blank to quit.\n")
    while True:
        try:
            text = input("review> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            return 0
        _show(classifier, text)


if __name__ == "__main__":
    raise SystemExit(main())

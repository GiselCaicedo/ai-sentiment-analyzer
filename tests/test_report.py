import json
from pathlib import Path

import pandas as pd

from sentiment_analyzer.classifier import Prediction
from sentiment_analyzer.cli import generate_report


class FakeClassifier:
    def predict(self, texts: list[str]) -> list[Prediction]:
        labels = {"Lovely": "positive", "Overcooked": "neutral", "It was fine": "neutral"}
        return [Prediction(labels.get(text, "negative"), 0.8) for text in texts]


def test_report_exports(tmp_path: Path, reviews: pd.DataFrame) -> None:
    source = tmp_path / "input.csv"
    reviews.to_csv(source, index=False)
    output = tmp_path / "data"
    reports = tmp_path / "reports"

    assert (
        generate_report(source, output, reports, classifier=FakeClassifier(), model_name="fake")
        == 4
    )
    result = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert result["model"] == "fake"
    assert result["counts"] == {"positive": 1, "neutral": 2, "negative": 1}
    assert result["evaluation"]["accuracy"] == 0.75
    assert result["evaluation"]["misclassified"][0]["review_id"] == 2
    assert "75.0%" in (reports / "feedback_report.md").read_text(encoding="utf-8")
    assert len(pd.read_csv(output / "reviews_scored.csv")) == 4
    assert len(list((reports / "charts").glob("*.png"))) == 3
